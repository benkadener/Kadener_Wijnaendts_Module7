"""Generate only the Phase 4 Steps 6–9 records; raw CSVs remain unchanged."""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
NAME='run_20261102_111005_367684_pi_kp1_ki0p08'
RAW=ROOT/'python/run_data'/f'{NAME}.csv'
COMMAND=RAW.with_name(NAME+'_commands.csv')
OUT=ROOT/'phase_4'
KEYS=['tec_C']+[f'rod{i}_C' for i in range(1,6)]
LABELS=['TEC (A0)','T1 (x = 0)','T2','T3','T4','T5']
COLORS=['#d95f02','#0072B2','#009E73','#CC79A7','#C49A00','#6A3D9A']

def main():
 rows=list(csv.DictReader(RAW.open()));cmd=list(csv.DictReader(COMMAND.open()))
 by_time={float(r['time_s']):r for r in cmd}
 assert len(by_time)==len(cmd),'Duplicate command timestamps'
 matched=[by_time[float(r['time_s'])] for r in rows]
 t=np.array([float(r['time_s']) for r in rows]);y=np.array([[float(r[k]) for k in KEYS] for r in rows])
 setpoint=np.array([float(r['gui_setpoint_C']) for r in matched])
 changes=np.flatnonzero((setpoint[1:]==45)&(setpoint[:-1]==20))+1
 assert len(changes)==1,'Expected one 20→45 C step'
 step=int(changes[0]);ts=t[step]
 slopes=np.full_like(y,np.nan)
 for i in range(len(t)):
  if i<step or t[i]-ts<120:continue
  j=max(step,np.searchsorted(t,t[i]-120));xx=t[j:i+1];xx=xx-xx.mean()
  slopes[i]=60*(xx[:,None]*(y[j:i+1]-y[j:i+1].mean(axis=0))).sum(axis=0)/(xx*xx).sum()
 good=np.all(np.abs(slopes)<.02,axis=1)
 start=None;best=(0.,None,None);interval=None
 for i,ok in enumerate(good):
  if ok and (i==0 or 0<t[i]-t[i-1]<=5):
   if start is None:start=i
   dur=t[i]-t[start]
   if dur>best[0]:best=(dur,float(t[start]),float(t[i]))
   if dur>=600 and interval is None:interval=(float(t[start]),float(t[i]))
  else:start=None
 for n in range(6,10):(OUT/f'step_{n}').mkdir(parents=True,exist_ok=True)
 def note(n,s):(OUT/f'step_{n}'/'README.md').write_text(s+'\n')
 note(6,'# Step 6: Numerical stationary criterion\n\nUse |dTi/dt| < 0.02 °C/min at all six sensors continuously for at least 600 s. Estimate drift with trailing 120 s ordinary least-squares fits at each recorded sample; do not let fitting windows cross the setpoint step. A data gap above 5 s breaks continuous acceptance. This operational window choice is documented here after acquisition; it is not evidence that the choice or prediction review was recorded before heating.\n\nPrediction inputs: h = 10 W/(m²·K) is provisional; d = 0.0127 m, L = 0.205 m, x = [0, 0.0275, 0.05, 0.10, 0.205] m. A cited k range and the preheating prediction record are still needed to establish the Biot, mL, and finite-length predictions. See the repository README for geometry uncertainties.')
 note(7,f'# Step 7: Continuous PI heating record\n\nRaw source: [CSV](../../python/run_data/{NAME}.csv); [command log](../../python/run_data/{NAME}_commands.csv). Both original files are retained unchanged.\n\nThe file starts at Arduino time {t[0]:.2f} s with a 20 °C command while the apparatus is cooling from the earlier pilot. The 20→45 °C PI step is recorded at {ts:.2f} s; acquisition continues to {t[-1]:.2f} s ({(t[-1]-ts)/60:.2f} min after the step). Kp = 1 PWM/°C and Ki = 0.08 PWM/(°C·s).\n\nThis includes a near-20 °C baseline before heating, but the rod has a spatial gradient under cooling; do not claim a common-bath agreement check from this baseline. No quantitative transient-model fit is required. The filename reflects its initial controller mode only; actual settings are read from the command log.')
 valid=np.flatnonzero(np.all(np.isfinite(slopes),axis=1))
 status='MET' if interval else 'NOT MET'
 summary=f'# Step 8: Temperature history and stationary check\n\n![Six-temperature history](temperature_history.png)\n\n**Criterion {status}.** '
 if interval:summary+=f'First qualifying interval: Arduino {interval[0]:.2f}–{interval[1]:.2f} s. '
 else:summary+='No accepted 10-minute stationary interval exists in the saved post-step record. '
 summary+=f'The longest simultaneous passing stretch is {best[0]:.2f} s.\n\n| Sensor | Final temperature (°C) | Final trailing-2-minute drift (°C/min) |\n|---|---:|---:|\n'
 for k,label in enumerate(LABELS):summary+=f'| {label} | {y[-1,k]:.2f} | {slopes[-1,k]:+.4f} |\n'
 summary+='\nA temperature profile cannot be labeled stationary solely from the last readings. Farther sensors respond later because heat must diffuse farther through the rod, and their changes are smaller because heat is lost along the side surface. The plot includes the entire recorded cooling/baseline and heating history; the command and measured TEC response should be assessed for overshoot rather than presumed non-oscillatory.\n'
 note(8,summary)
 with (OUT/'step_8/stationarity_check.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['time_s']+[k+'_drift_C_per_min' for k in KEYS]+['all_sensors_pass'])
  for i in valid:w.writerow([t[i],*slopes[i],int(good[i])])
 fig,ax=plt.subplots(figsize=(11,6),constrained_layout=True)
 for k,(label,color) in enumerate(zip(LABELS,COLORS)):ax.plot(t/60,y[:,k],label=label,color=color,lw=2 if k==0 else 1.3)
 ax.step(t/60,setpoint,where='post',color='black',ls='--',label='TEC command')
 ax.axvline(ts/60,color='.4',ls=':',label='20→45 °C step')
 if interval:ax.axvspan(interval[0]/60,interval[1]/60,color='green',alpha=.15,label='Accepted stationary interval')
 ax.set(xlabel='Arduino elapsed time (min)',ylabel='Temperature (°C)',title=f'Phase 4: full temperature history — stationarity {status.lower()}')
 ax.grid(alpha=.25);ax.legend(ncol=2,fontsize=8);fig.savefig(OUT/'step_8/temperature_history.png',dpi=180);plt.close(fig)
 with (OUT/'step_9/boundary_temperatures.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['time_s','commanded_tec_C','measured_tec_C','rod_base_T0_C'])
  for r,c in zip(rows,matched):w.writerow([r['time_s'],c['gui_setpoint_C'],r['tec_C'],r['rod1_C']])
 note(9,'# Step 9: Boundary temperatures\n\n[Saved boundary record](boundary_temperatures.csv) contains the commanded TEC temperature from the matched command log, measured TEC temperature from A0, and measured rod-base temperature T(0,t) from T1/A1. Original Arduino timestamps are retained.\n\n**T1 at x = 0 supplies the rod model boundary condition.** The TEC setpoint and A0 temperature are separate signals and must not substitute for it. Raw setpoint_C remains nan; the GUI command log provides commanded_tec_C without changing the raw data. Ambient temperature is not recorded by these six attached sensors; measure it separately.')
 print('Step time',ts,'status',status,'longest',best,'last slopes',slopes[-1])
 print('Created phase_4/step_6 through step_9.')
if __name__=='__main__':main()
