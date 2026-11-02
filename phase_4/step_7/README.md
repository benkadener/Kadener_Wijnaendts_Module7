# Step 7: Continuous PI heating record

Raw source: [CSV](../../python/run_data/run_20261102_111005_367684_pi_kp1_ki0p08.csv); [command log](../../python/run_data/run_20261102_111005_367684_pi_kp1_ki0p08_commands.csv). Both original files are retained unchanged.

The file starts at Arduino time 2698.96 s with a 20 °C command while the apparatus is cooling from the earlier pilot. The 20→45 °C PI step is recorded at 3815.24 s; acquisition continues to 5100.69 s (21.42 min after the step). Kp = 1 PWM/°C and Ki = 0.08 PWM/(°C·s).

This includes a near-20 °C baseline before heating, but the rod has a spatial gradient under cooling; do not claim a common-bath agreement check from this baseline. No quantitative transient-model fit is required. The filename reflects its initial controller mode only; actual settings are read from the command log.
