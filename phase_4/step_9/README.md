# Step 9: Boundary temperatures

[Saved boundary record](boundary_temperatures.csv) contains the commanded TEC temperature from the matched command log, measured TEC temperature from A0, and measured rod-base temperature T(0,t) from T1/A1. Original Arduino timestamps are retained.

**T1 at x = 0 supplies the rod model boundary condition.** The TEC setpoint and A0 temperature are separate signals and must not substitute for it. Raw setpoint_C remains nan; the GUI command log provides commanded_tec_C without changing the raw data. Ambient temperature is not recorded by these six attached sensors; measure it separately.
