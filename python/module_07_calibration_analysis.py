"""Fit relative thermistor corrections without changing the raw acquisition CSV.

Examples (run from the Module 7 repository):
  python3 python/module_07_calibration_analysis.py python/run_data/bath.csv --temperature-range 22 45
  python3 python/module_07_calibration_analysis.py python/run_data/bath.csv --time-range 60 600

Both ranges may be given; their intersection is used. With neither, all finite
pairs are fitted. Use common-bath data with all six sensors connected, not rod
heating data. These are relative corrections to A0, not absolute calibration.
"""

import argparse
import csv
import math
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Save plots without needing an open plotting window.
import matplotlib.pyplot as plt

RAW_COLUMNS = (
    "time_s", "tec_C", "rod1_C", "rod2_C", "rod3_C", "rod4_C", "rod5_C",
    "pwm", "heat_cool", "setpoint_C", "safety",
)
ROD_COLUMNS = RAW_COLUMNS[2:7]
SUMMARY_COLUMNS = (
    "channel", "a_i_C", "b_i", "n_fitted_points", "calibration_min_tec_C",
    "calibration_max_tec_C", "residual_mean_C", "residual_std_C",
    "max_absolute_residual_C",
)


def numeric(rows, column):
    """Convert a column for calculations; keep the original text untouched."""
    values = []
    for row in rows:
        try:
            values.append(float(row[column]))
        except (TypeError, ValueError):
            values.append(float("nan"))
    return np.asarray(values)


def load_raw(path):
    # FILE INPUT: read only, retaining every original column and cell value.
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        if not columns or len(set(columns)) != len(columns):
            raise ValueError("CSV must have unique named columns.")
        missing = set(RAW_COLUMNS) - set(columns)
        if missing:
            raise ValueError(f"Missing raw columns: {', '.join(sorted(missing))}")
        if any(f"rod{i}_corrected_C" in columns for i in range(1, 6)):
            raise ValueError("Choose an original raw CSV, not an already corrected file.")
        rows = list(reader)
        if not rows:
            raise ValueError("CSV contains no data rows.")
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError("CSV has incomplete rows or extra fields; raw file left unchanged.")
    return columns, rows


def fit_channels(rows, time_range=None, temperature_range=None):
    # RANGE SELECTION: inclusive limits; temperature limits refer to TEC/A0.
    reference = numeric(rows, "tec_C")
    selected = np.isfinite(reference)
    if time_range is not None:
        time = numeric(rows, "time_s")
        selected &= np.isfinite(time) & (time >= time_range[0]) & (time <= time_range[1])
    if temperature_range is not None:
        selected &= (reference >= temperature_range[0]) & (reference <= temperature_range[1])

    fits = []
    for channel in ROD_COLUMNS:
        rod = numeric(rows, channel)
        mask = selected & np.isfinite(rod)
        x, y = rod[mask], reference[mask]
        if len(x) < 3 or np.ptp(x) < 1e-6 or np.ptp(y) < 1e-6:
            raise ValueError(f"{channel}: need at least 3 finite points spanning varying rod and TEC temperatures.")

        # FITTING: solve TEC = a + b*rod. Centering improves numerical accuracy.
        design = np.column_stack((np.ones(len(x)), x - x.mean()))
        coefficients, _, rank, _ = np.linalg.lstsq(design, y, rcond=None)
        if rank != 2:
            raise ValueError(f"{channel}: calibration fit is rank deficient.")
        b = float(coefficients[1])
        a = float(coefficients[0] - b * x.mean())

        # RESIDUALS: corrected rod minus TEC, evaluated on fitted points only.
        residual = (a + b * x) - y
        summary = dict(zip(SUMMARY_COLUMNS, (
            channel, a, b, len(x), float(y.min()), float(y.max()),
            float(residual.mean()), float(residual.std(ddof=1)),
            float(np.max(np.abs(residual))),
        )))
        fits.append((summary, x, y, residual))
    return fits


def save_outputs(output, columns, rows, fits):
    # OUTPUT: output is a freshly created directory. Never open the raw CSV for writing.
    with (output / "calibration_coefficients.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(fit[0] for fit in fits)

    corrected_columns = [f"rod{i}_corrected_C" for i in range(1, 6)]
    with (output / "corrected_data.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns + corrected_columns)
        writer.writeheader()
        for raw in rows:
            result = dict(raw)  # Retain EVERY raw field, including nan setpoints.
            for corrected, (summary, _, _, _) in zip(corrected_columns, fits):
                try:
                    value = float(raw[summary["channel"]])
                    corrected_value = summary["a_i_C"] + summary["b_i"] * value
                    result[corrected] = corrected_value if math.isfinite(corrected_value) else "nan"
                except (ValueError, TypeError):
                    result[corrected] = "nan"
            writer.writerow(result)

    for summary, rod, reference, residual in fits:
        a, b = summary["a_i_C"], summary["b_i"]
        channel = summary["channel"]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
        # Rod against TEC: x=TEC, y=raw rod. Parameterize the fitted line
        # by rod temperature: (x, y) = (a+b*rod, rod), avoiding division by b.
        axes[0].scatter(reference, rod, s=8, alpha=.45, label="Raw fitted points")
        limits = [float(min(reference.min(), rod.min())), float(max(reference.max(), rod.max()))]
        axes[0].plot(limits, limits, "k--", label="Identity: rod = TEC")
        rod_line = np.linspace(rod.min(), rod.max(), 200)
        axes[0].plot(a + b * rod_line, rod_line, color="tab:orange", label="Fit: TEC = a + b·rod")
        axes[0].set_xlabel("TEC reference temperature (°C)")
        axes[0].set_ylabel(f"Raw {channel.removesuffix('_C')} temperature (°C)")
        axes[0].legend(fontsize=8)
        axes[1].scatter(reference, residual, s=8, alpha=.45)
        axes[1].axhline(0, color="black", ls="--")
        axes[1].set_xlabel("TEC reference temperature (°C)")
        axes[1].set_ylabel("Corrected rod − TEC residual (°C)")
        for ax in axes:
            ax.grid(alpha=.25)
        fig.suptitle(f"{channel}: a = {a:.5g} °C, b = {b:.6g}, n = {len(rod)}")
        fig.savefig(output / f"{channel.removesuffix('_C')}_calibration.png", dpi=180)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--time-range", nargs=2, type=float, metavar=("MIN_S", "MAX_S"))
    parser.add_argument("--temperature-range", nargs=2, type=float, metavar=("MIN_C", "MAX_C"))
    parser.add_argument("--output-dir", type=Path, help="New directory only; must not already exist.")
    args = parser.parse_args()
    for limits in (args.time_range, args.temperature_range):
        if limits is not None and (not all(math.isfinite(v) for v in limits) or limits[0] > limits[1]):
            parser.error("Range bounds must be finite and ordered minimum to maximum.")
    try:
        columns, rows = load_raw(args.csv_file)
        fits = fit_channels(rows, args.time_range, args.temperature_range)
        if args.output_dir:
            output = args.output_dir
            output.mkdir(parents=True, exist_ok=False)
        else:
            # mkdtemp guarantees a unique run directory, even with concurrent runs.
            output = Path(tempfile.mkdtemp(
                prefix=f"{args.csv_file.stem}_calibration_{datetime.now():%Y%m%d_%H%M%S}_",
                dir=args.csv_file.resolve().parent,
            ))
        save_outputs(output, columns, rows, fits)
        (output / "selection.txt").write_text(
            f"Raw input: {args.csv_file.resolve()}\nTime range (s): {args.time_range}\n"
            f"TEC range (°C): {args.temperature_range}\n"
            "Bounds inclusive; ranges intersect. Nonfinite pairs excluded per channel.\n"
            "Residual statistics are in-sample; standard deviation uses ddof=1.\n"
            "Corrections applied to all rows; outside the fitted range they are extrapolations.\n"
        )
    except (OSError, ValueError) as error:
        parser.exit(1, f"Calibration failed: {error}\n")
    # Print the complete same table saved to calibration_coefficients.csv.
    print(",".join(SUMMARY_COLUMNS))
    for summary, _, _, _ in fits:
        print(",".join(str(summary[key]) for key in SUMMARY_COLUMNS))
    print(f"\nSaved outputs: {output.resolve()}")


if __name__ == "__main__":
    main()
