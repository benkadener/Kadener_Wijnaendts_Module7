# Module 7: Stationary rod experiment

## Measured geometry and sensor map

Reported rod material: 6061-T6 aluminum. Diameter d = 12.7 mm = 0.0127 m; radius R = 0.00635 m. Analysis length L = 20.5 cm = 0.205 m, measured from T1 to the tip. Positive x runs from T1 toward T5/the tip. A0 is the separate TEC-base sensor, not the rod coordinate origin.

| Sensor | Arduino pin | Distance from T1 (cm) | x (m) | x/L |
|---|---|---:|---:|---:|
| T1 | A1 | 0 | 0 | 0 |
| T2 | A2 | 2.75 ± 0.10 | 0.0275 | 0.1341 |
| T3 | A3 | 5.00 ± 0.10 | 0.0500 | 0.2439 |
| T4 | A4 | 10.00 ± 0.10 | 0.1000 | 0.4878 |
| T5 (reported tip position) | A5 | 20.50 ± 0.10 | 0.2050 | 1.0000 |

For a circular rod:

- Cross-sectional area: A = πd²/4 = **1.26677 × 10⁻⁴ m²**.
- Perimeter: P = πd = **0.0398982 m**.
- Side surface area over the analysis length: PL = **0.00817914 m²**.
- Transverse characteristic length: A/P = d/4 = **0.003175 m**.

### Measurement tools and uncertainties

- Ruler smallest division: **1 mm = 0.10 cm**. A clearly located endpoint is estimated to ±0.5 mm; adding the two endpoint bounds gives a conservative distance uncertainty of **±1 mm = ±0.10 cm**.
- Analysis length: **L = (20.50 ± 0.10) cm = (0.2050 ± 0.0010) m**.
- T2–T5 position uncertainties are **±0.10 cm = ±0.0010 m**, as listed above. T1 defines x = 0; uncertainty in locating T1 contributes to all relative distances. Increase the bounds if sensing centers cannot be located this precisely.
- Diameter measured with calipers: **d = 1.2700 cm**. Reported caliper specification: **0.025 mm = 0.0025 cm**. The user confirmed this is the stated measurement error. Use **d = (1.2700 ± 0.0025) cm = (0.012700 ± 0.000025) m**.
- The bounds above are practical measurement estimates, not established one-standard-deviation uncertainties. Shared-origin position errors are correlated; T5 and L must not be treated as independent measurements if both refer to the same tip location.

Geometry values above use nominal dimensions. Their extra digits describe calculation precision, not measurement accuracy.

## Provisional A4 calculation setup

With h = 10 W/(m²·K), measured geometry gives

$$
m=\sqrt{\frac{hP}{kA}}=\sqrt{\frac{4h}{kd}},\qquad
m^2=\frac{3149.6063}{k_{\mathrm{num}}}\ \mathrm{m}^{-2},\qquad
mL=0.205\sqrt{\frac{3149.6063}{k_{\mathrm{num}}}},
$$

where k_num is the numerical conductivity in W/(m·K). The decay length is 1/m. Dimensionally, hP/(kA) has units m⁻², so m has units m⁻¹ and mL is dimensionless.

Using the transverse A/P convention,

$$
\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}=\frac{0.03175}{k_{\mathrm{num}}}.
$$

The separate radius-based quantity is hR/k = 0.0635/k_num (twice the A/P-based Biot number). Both are dimensionless. A numerical literature conductivity range is still needed before calculating the requested m, mL, decay-length, and Biot ranges.

For the insulated-tip model and semi-infinite approximation at the same m and base excess θb:

$$
\theta_{\mathrm{finite}}(x)=\theta_b\frac{\cosh[m(L-x)]}{\cosh(mL)},\qquad
\theta_{\infty}(x)=\theta_b e^{-mx}.
$$

A relative error measured against the finite solution is

$$
\epsilon_T(x)=\frac{|\theta_{\mathrm{finite}}(x)-\theta_{\infty}(x)|}{|\theta_{\mathrm{finite}}(x)|}
=\frac{e^{-2m(L-x)}-e^{-2mL}}{1+e^{-2m(L-x)}}.
$$

Evaluate at x = 0, 0.0275, 0.0500, 0.1000, and 0.2050 m using both ends of the cited k range. Confirm the course's error normalization before final A4 assembly. These theory calculations do not require experimental temperature data.

## Information still to record

- Overall physical rod length; confirm T5 position is measured at the sensor center and whether the caliper specification is accuracy or resolution.
- Labeled sensor-map photograph.
- Common-bath results at the tested temperatures. No correction is needed only if the spread stayed below 1 °C throughout the check.
- Final chosen stationary interval and measured room temperature.
- Exact Git checkpoint for the sketch, GUI, and analysis used.

## A4 versus experimental record

A4 is an individual pre-experiment theory PDF. It uses measured geometry, planned sensor positions, a cited aluminum conductivity range, and provisional h = 10 W/(m²·K). It does not require experimental temperature CSVs or fitted profiles. Source: `docs/assessments/a4_finite_length_biot.md`; submission: `A4_Lastname.pdf`, due November 9, 2026 at 9:05 AM.

The experimental stationary-fin record belongs at `docs/module_notes/module_07_stationary_fin.md`, with authoritative analysis under `python/analysis/`. Retain the full time history, stationary excess temperatures, finite and semi-infinite fits and residuals, fitted m and 1/m with uncertainty, finite-length errors, and transverse Biot check. The final prescribed acquisition follows equilibration at 20 °C and a recorded PI step to 45 °C.

## Latest 45 °C placement-pilot results

- Raw record: [CSV](python/run_data/run_20261102_102500_325095_manual_kp1_ki0p08.csv); [GUI command log](python/run_data/run_20261102_102500_325095_manual_kp1_ki0p08_commands.csv).
- Screenshot: [45C_steady_state.png](45C_steady_state.png).
- Ambient temperature used: **23.5 °C**, user supplied; ambient uncertainty not yet recorded.
- The CSV contains 2177 samples from 0.75 to 1585.36 s. The final values below are later than the screenshot.
- Final command log confirms PI, setpoint 45 °C, Kp = 1 PWM/°C, Ki = 0.08 PWM/(°C·s). The filename contains `manual` because it reflects the mode when the file was created, not necessarily later controller settings.

| Sensor | Final reading (°C) | Final excess above 23.5 °C (°C) | Last-10-minute mean (°C) | Fitted drift (°C/min) |
|---|---:|---:|---:|---:|
| TEC (A0) | 45.06 | 21.56 | 45.041 | +0.0175 |
| T1 | 40.98 | 17.48 | 40.621 | +0.0476 |
| T2 | 38.86 | 15.36 | 38.411 | +0.0622 |
| T3 | 37.71 | 14.21 | 37.202 | +0.0698 |
| T4 | 35.51 | 12.01 | 34.885 | +0.0803 |
| T5 | 32.72 | 9.22 | 32.007 | +0.0909 |

Final sample at **1585.36 s**: actual PWM = 46, heat_cool = 1 (heating), safety = OK. Arduino `setpoint_C=nan` is preserved as raw data; the paired command log records the actual GUI setpoint.

**Stationarity not established:** drift estimates use ordinary least-squares fits over 985.96–1585.36 s (9.990 min). Every rod channel exceeds the 0.02 °C/min threshold even over this full-window average. This summary does not test continuous compliance in shorter windows, and these means must not be called accepted stationary temperatures. T3 also contains short downward spikes that should be checked.

**Placement check using the final sample:** θ5/θ1 = (32.72 − 23.5)/(40.98 − 23.5) = **0.5275**, greater than 1/e = 0.3679. At this T1 value the required T5 upper bound would be **29.93 °C**. This is a provisional check because the rod is still drifting. With T5 already at x = L, discuss the unmet placement condition with the instructor rather than assuming a farther hole exists.

Keep both full CSVs unchanged as pilot evidence. Verify stationarity and resolve sensor placement before using a stationary profile for fitting; the prescribed final run is a continuously recorded 20→45 °C step after equilibration at 20 °C.


## Placement decision and latest displayed readings

The team reports that T1–T5 are spread across the maximum available hole separation; T5 is at the reported analysis tip, x = L = 0.205 m. No farther position is available in this apparatus. Retain these positions and report the limited spatial temperature drop rather than claiming the placement criterion passed. Ask the instructor whether this geometry is acceptable for the remaining measurements.

Latest user-supplied display snapshot (Arduino timestamp not supplied):

| Sensor | Temperature (°C) |
|---|---:|
| TEC (A0) | 45.09 |
| T1 | 40.54 |
| T2 | 38.23 |
| T3 | 37.01 |
| T4 | 34.74 |
| T5 | 32.07 |

Using provisional ambient 23.5 °C, θ1 = 17.04 °C and θ5 = 8.57 °C; θ5/θ1 = **0.5029**, above 1/e = 0.3679. This snapshot does not establish the required stationary interval. Ambient must be measured independently; it is not the 20 °C TEC setpoint. These display readings are distinct from the earlier timestamped CSV summary.

## Next acquisition steps

1. Measure room air temperature near the apparatus, away from heat sources and exhaust; record its uncertainty. Keep the fixed sensor positions and their uncertainties documented.
2. Preserve the pilot raw CSV and paired command log. Check the complete time history for stationarity and record the spatial-range limitation; do not claim a passed placement criterion.
3. Set the TEC to 20 °C using PI and let the entire rod equilibrate. Record the six-channel baseline and assess the rod-channel agreement required by the lab; investigate any disagreement rather than forcing corrections from a real rod gradient.
4. Before the final step, review the prediction record. Use provisional h = 10 W/(m²·K) and record the chosen stationary criterion: every sensor's temperature drift below 0.02 °C/min for at least 10 minutes, or justify a different criterion.
5. Start a fresh raw/command CSV pair while at the equilibrated baseline. The New run CSV button zeros PWM and clears the integral, so allow the 20 °C PI baseline to re-establish before changing the setpoint. Record baseline and the complete 20→45 °C step continuously without starting another file at the step.
6. Keep sensors and gains fixed, never exceed the lab's 55 °C limit, and continue until the chosen stationary criterion is met. Save the full raw CSV and matching command CSV.
7. Analyze the complete temperature history, justify the stationary interval, and make the semilog placement plot and finite/semi-infinite profile fits with residuals. Retain the unmet 1/e criterion as a limitation of the available geometry.
