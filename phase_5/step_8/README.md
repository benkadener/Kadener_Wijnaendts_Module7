# Step 8: Systematic errors and tip evidence

- Position error: ruler distances have ±0.001 m bounds, with common-origin correlation. Diameter has a provisional ±0.000025 m bound; confirm caliper accuracy. The fit uses positions/L, not diameter. A 400-draw sensitivity exercise perturbs endpoint readings uniformly within ±0.5 mm and ties T5 to L; it is illustrative, not a measured error distribution.
  - finite_insulated_tip: position-sensitivity SD in m = 0.0150 m⁻¹; changing ambient from 23 to 24 °C gives m = 5.6829 to 5.9428 m⁻¹.
  - semi_infinite: position-sensitivity SD in m = 0.0093 m⁻¹; changing ambient from 23 to 24 °C gives m = 3.3045 to 3.5741 m⁻¹.
- Room drift: no independent ambient time series or ambient uncertainty was saved. The ±0.5 °C exercise is a sensitivity scenario, not an uncertainty measurement. A constant ambient offset changes every excess together.
- Imperfect contact: unknown hole contact, sensor depth, and conduction along leads can bias individual channels. T3 has downward spikes; no points were silently deleted or calibrated.
- Tip: a finite model assumes zero axial gradient at the tip, while real end-face convection/radiation may remove heat. The final T4→T5 secant slope is not a measurement of the derivative exactly at L. One tip-adjacent sensor and a changing profile cannot establish an insulated boundary.
- Thermal drift: the final averaging interval is still evolving, with especially large distal drift. This is a principal unresolved error, not just random scatter.
