# Module 7: Rod instrument and Phase 5 evidence

**PROVISIONAL — stationarity not met.** These results are a reproducible late-time comparison, not completed stationary validation.

## Evidence index

- [Phase 5 step 1](../../phase_5/step_1/README.md)
- [Phase 5 step 2](../../phase_5/step_2/README.md)
- [Phase 5 step 3](../../phase_5/step_3/README.md)
- [Phase 5 step 4](../../phase_5/step_4/README.md)
- [Phase 5 step 5](../../phase_5/step_5/README.md)
- [Phase 5 step 6](../../phase_5/step_6/README.md)
- [Phase 5 step 7](../../phase_5/step_7/README.md)
- [Phase 5 step 8](../../phase_5/step_8/README.md)
- [Phase 5 step 9](../../phase_5/step_9/README.md)

## Acquisition and sensor map

- [Raw record](../../python/run_data/run_20261102_111005_367684_pi_kp1_ki0p08.csv) and [command log](../../python/run_data/run_20261102_111005_367684_pi_kp1_ki0p08_commands.csv); originals unchanged.
- A0: TEC base and sole feedback/safety sensor. A1–A5: T1–T5 at x = [0, 0.0275, 0.0500, 0.1000, 0.2050] m. T1 is the rod boundary at x = 0; T5 is the reported tip.
- Material: 6061-T6 aluminum, d = 0.0127 m, L = 0.205 m. Ruler distance bounds ±0.001 m; provisional caliper diameter bound ±0.000025 m. See [repository notes](../../README.md).
- Common-bath completion/pass was reported by the user; quantitative observations and a labeled map photograph are not available in this analysis. No corrections were applied.
- Ambient 23.5 °C is user supplied, without an independently logged time history or uncertainty.

## Reproduction and checkpoint

`python3 python/analysis/analyze_phase5.py`

Repository HEAD at analysis: `570def64d01d90302ef2e5854dbf9d2bf512818e`. This is not certification that the current acquisition/analysis files are committed. [Input and code hashes](../../data/module_07/phase_5/provenance.csv) identify the exact analyzed contents. No raw data were overwritten.

## Outstanding evidence

- A qualifying stationary interval (or instructor-approved alternative criterion with justification).
- Quantitative common-bath record, labeled sensor-map photo, and independently measured ambient with uncertainty.
- Completed preheating predictions and exact committed acquisition-code checkpoint.
- Do not present the finite/exponential parameter errors as full uncertainty while thermal drift and ambient error remain unresolved.
