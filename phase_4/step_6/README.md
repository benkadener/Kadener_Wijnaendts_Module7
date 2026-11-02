# Step 6: Numerical stationary criterion

Use |dTi/dt| < 0.02 °C/min at all six sensors continuously for at least 600 s. Estimate drift with trailing 120 s ordinary least-squares fits at each recorded sample; do not let fitting windows cross the setpoint step. A data gap above 5 s breaks continuous acceptance. This operational window choice is documented here after acquisition; it is not evidence that the choice or prediction review was recorded before heating.

Prediction inputs: h = 10 W/(m²·K) is provisional; d = 0.0127 m, L = 0.205 m, x = [0, 0.0275, 0.05, 0.10, 0.205] m. A cited k range and the preheating prediction record are still needed to establish the Biot, mL, and finite-length predictions. See the repository README for geometry uncertainties.
