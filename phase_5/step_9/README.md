# Step 9: Compare with predictions and assess adequacy

The late profile decreases with x, consistent with axial conduction plus side heat loss. Both models are fitted, without assuming a semi-infinite rod. For this provisional interval, **finite insulated tip** has the smaller nonbase RMSE. This ranks only the present curve shapes; it is not a validated stationary-model conclusion.

With finite-fit mL = 1.191, the relative difference |θ_f − θ_infinity|/|θ_f| at the same finite-fit m reaches 45.4% at T5. [Sensor-by-sensor errors](../../data/module_07/phase_5/finite_length_error.csv) separate finite-end approximation error from differences between independently fitted m values. The observed tip/base excess ratio is 0.528, above 1/e; maximum available separation is documented, not a passed placement test.

There is no completed quantitative preheating prediction record with a cited k range, so an agreement claim against such a prediction cannot yet be made. Revisit it when available. Constant h, uniform cross-section, negligible radial gradients, negligible radiation, and an insulated tip remain assumptions, not established facts. Radial adequacy requires a separate Biot check; a longitudinal fit alone cannot test it. Unexplained effects include the evolving distal temperatures and sensor-specific spikes.

A fitted m constrains m² = hP/(kA), hence h/k; it cannot independently separate k and h. Units: hP/(kA) is m⁻², m is m⁻¹, and 1/m is m.

The stationary equation is kA d²T/dx² − hP(T − Tamb) = 0, assuming steady one-dimensional conduction, constant k/h/A/P, no internal generation, and uniform ambient. Boundary conditions are θ(0) = measured θb and dθ/dx(L) = 0 for the finite insulated-tip model; the semi-infinite model replaces the latter by θ→0 as x→∞.
