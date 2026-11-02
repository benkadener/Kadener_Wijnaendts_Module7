"""Phase 5 fin comparison. Raw acquisition files are opened read-only.

Run from Module 7: python3 python/analysis/analyze_phase5.py
Outputs are provisional unless the Phase 4 stationarity criterion passes.
No calibration correction or quantitative transient fit is performed.
"""
import csv
import hashlib
import subprocess
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
RUN='run_20261102_111005_367684_pi_kp1_ki0p08'
RAW=ROOT/'python/run_data'/f'{RUN}.csv'
COMMAND=RAW.with_name(RUN+'_commands.csv')
OUT=ROOT/'phase_5'
DATA=ROOT/'data/module_07/phase_5'
FIG=ROOT/'docs/figures/module_07'
AMBIENT=23.5  # User supplied, not independently recorded in this acquisition.
X=np.array([0.,.0275,.05,.1,.205])
L=.205
D=.0127
KEYS=['tec_C']+[f'rod{i}_C' for i in range(1,6)]


def save_csv(path, fields, rows):
    with path.open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(fields);writer.writerows(rows)


def response(m, x=X, length=L, finite=True):
    # Stable form of cosh[m(L-x)]/cosh(mL); avoids cosh overflow.
    if finite:
        return (np.exp(-m*x)+np.exp(-m*(2*length-x)))/(1+np.exp(-2*m*length))
    return np.exp(-m*x)


def fit_m(theta, x=X, length=L, finite=True):
    # One fitted parameter m>0, with measured T1 fixing theta_b.
    # Golden-section minimization in log(m) needs only NumPy.
    def loss(logm):
        residual=theta[0]*response(np.exp(logm),x,length,finite)-theta
        return float(np.sum(residual[1:]**2))
    lo,hi=np.log(1e-5),np.log(1000.)
    ratio=(np.sqrt(5)-1)/2
    a=hi-ratio*(hi-lo);b=lo+ratio*(hi-lo)
    fa,fb=loss(a),loss(b)
    for _ in range(85):
        if fa<fb:
            hi,b,fb=b,a,fa;a=hi-ratio*(hi-lo);fa=loss(a)
        else:
            lo,a,fa=a,b,fb;b=lo+ratio*(hi-lo);fb=loss(b)
    return float(np.exp((lo+hi)/2))


def check_stationarity(t, temperatures, step_time):
    slopes=np.full_like(temperatures,np.nan)
    for i,ti in enumerate(t):
        if ti-step_time<120:continue
        j=np.searchsorted(t,ti-120)
        xx=t[j:i+1];xx=xx-xx.mean()
        slopes[i]=60*(xx[:,None]*(temperatures[j:i+1]-temperatures[j:i+1].mean(axis=0))).sum(axis=0)/(xx*xx).sum()
    passing=np.all(np.abs(slopes)<.02,axis=1)
    start=None;accepted=None;longest=0.
    for i,ok in enumerate(passing):
        if ok and (i==0 or 0<t[i]-t[i-1]<=5):
            if start is None:start=i
            longest=max(longest,t[i]-t[start])
            if t[i]-t[start]>=600:accepted=(t[start],t[i])
        else:start=None
    return accepted,longest,slopes


def main():
    for folder in [DATA,FIG,ROOT/'docs/module_notes']+[OUT/f'step_{i}' for i in range(1,10)]:folder.mkdir(parents=True,exist_ok=True)
    raw_bytes=RAW.read_bytes();command_bytes=COMMAND.read_bytes()
    rows=list(csv.DictReader(raw_bytes.decode().splitlines()));commands=list(csv.DictReader(command_bytes.decode().splitlines()))
    command_by_time={float(r['time_s']):r for r in commands}
    t=np.array([float(r['time_s']) for r in rows]);temps=np.array([[float(r[k]) for k in KEYS] for r in rows])
    sp=np.array([float(command_by_time[ti]['gui_setpoint_C']) for ti in t])
    steps=np.flatnonzero((sp[1:]==45)&(sp[:-1]==20))+1
    if len(steps)!=1:raise ValueError('Expected exactly one recorded 20→45 C step.')
    step_time=t[steps[0]]
    accepted,longest,slopes=check_stationarity(t,temps,step_time)
    # Use an accepted final 5-minute interval if available; otherwise disclose
    # that this is only an illustrative late-time average, not stationary data.
    end=float(accepted[1]) if accepted else float(t[-1])
    mask=(t>=end-300)&(t<=end)&(t>=step_time)
    tm=t[mask];v=temps[mask]
    means=v.mean(axis=0);sd=v.std(axis=0,ddof=1)
    drift=np.array([np.polyfit(tm-tm[0],v[:,i],1)[0]*60 for i in range(6)])
    theta=means[1:]-AMBIENT
    if np.any(theta<=0):raise ValueError('All fitted excess temperatures must be positive.')
    provisional=not bool(accepted)
    state='PROVISIONAL — stationarity not met' if provisional else 'Stationarity met'
    notes={}
    notes[1]=f'# Step 1: Select and check interval\n\n**{state}.** The saved post-step record has no accepted interval.' if provisional else f'# Step 1: Select and check interval\n\n{state}.'
    notes[1]+=f' The longest all-sensor passing stretch is {longest:.2f} s, versus the required 600 s. Criterion: all six |dT/dt| < 0.02 °C/min using trailing 120 s linear fits; gaps over 5 s break acceptance. The step occurs at {step_time:.2f} s. No separate heating run was used.\n\nFinal analysis interval: {tm[0]:.2f}–{tm[-1]:.2f} s ({tm[-1]-tm[0]:.2f} s). '+('This is the final available five minutes, chosen for a provisional comparison; it is not an approved replacement criterion.' if provisional else 'This is a final five-minute interval after the criterion was met.')
    save_csv(DATA/'averaged_profile.csv',['sensor','x_m','position_bound_m','mean_temperature_C','temporal_sd_C','fitted_drift_C_per_min','ambient_C','excess_C'],
             [[f'T{i+1}',X[i],0 if i==0 else .001,means[i+1],sd[i+1],drift[i+1],AMBIENT,theta[i]] for i in range(5)])
    notes[2]=f'# Step 2: Average temperatures\n\n[Profile CSV](../../data/module_07/phase_5/averaged_profile.csv), n = {len(tm)} samples over {tm[0]:.2f}–{tm[-1]:.2f} s. Ambient assumed constant at {AMBIENT} °C, user supplied. Error bars use temporal sample standard deviations, not standard errors or calibrated absolute uncertainty. Samples are correlated and the data drift; small standard errors would misrepresent the uncertainty.\n\n| Sensor | Mean (°C) | Temporal SD (°C) | Drift (°C/min) |\n|---|---:|---:|---:|\n'
    for i,key in enumerate(KEYS):notes[2]+=f'| {key} | {means[i]:.3f} | {sd[i]:.3f} | {drift[i]:+.4f} |\n'
    models=[]
    for finite,name in [(True,'finite_insulated_tip'),(False,'semi_infinite')]:
        m=fit_m(theta,finite=finite);pred=theta[0]*response(m,finite=finite);res=theta-pred
        # Conditional linearized regression uncertainty from residual variance.
        # T1 is fixed, leaving 4 independent fitted residuals and 3 degrees of freedom.
        eps=m*1e-5
        jac=theta[0]*(response(m+eps,finite=finite)-response(m-eps,finite=finite))/(2*eps)
        se=float(np.sqrt(np.sum(res[1:]**2)/3/np.sum(jac[1:]**2)))
        models.append(dict(name=name,finite=finite,m=m,se=se,length=1/m,length_se=se/m**2,pred=pred,res=res,rmse=float(np.sqrt(np.mean(res[1:]**2)))))
    # Geometry sensitivity: one shared T1 endpoint, separate other endpoints,
    # and T5 tied to L. ±0.5 mm endpoint bounds imply ±1 mm distance bounds.
    rng=np.random.default_rng(7);mc=[[],[]]
    for _ in range(400):
        endpoints=rng.uniform(-.0005,.0005,6)
        xp=X.copy();xp[1:]+=endpoints[2:6]-endpoints[0]
        lp=xp[-1]
        for j,model in enumerate(models):mc[j].append(fit_m(theta,xp,lp,model['finite']))
    for j,model in enumerate(models):
        model['position_sensitivity_sd']=float(np.std(mc[j],ddof=1))
        model['ambient_low']=fit_m(means[1:]-(AMBIENT-.5),finite=model['finite'])
        model['ambient_high']=fit_m(means[1:]-(AMBIENT+.5),finite=model['finite'])
    save_csv(DATA/'fit_parameters.csv',['model','m_per_m','conditional_fit_se_per_m','decay_length_m','conditional_decay_length_se_m','rmse_nonbase_C','position_sensitivity_sd_per_m','m_at_ambient_23_C','m_at_ambient_24_C'],
             [[d['name'],d['m'],d['se'],d['length'],d['length_se'],d['rmse'],d['position_sensitivity_sd'],d['ambient_low'],d['ambient_high']] for d in models])
    save_csv(DATA/'model_residuals.csv',['sensor','x_m','measured_excess_C','finite_prediction_C','finite_residual_C','semi_infinite_prediction_C','semi_infinite_residual_C'],
             [[f'T{i+1}',X[i],theta[i],models[0]['pred'][i],models[0]['res'][i],models[1]['pred'][i],models[1]['res'][i]] for i in range(5)])
    xx=np.linspace(0,L,300)
    fig,ax=plt.subplots(figsize=(8,5),constrained_layout=True)
    ax.errorbar(X,theta,yerr=sd[1:],xerr=[0,.001,.001,.001,.001],fmt='o',color='black',capsize=3,label='Late means ± temporal SD; x bounds ±1 mm')
    for d in models:ax.plot(xx,theta[0]*response(d['m'],xx,finite=d['finite']),label=d['name'].replace('_',' '))
    ax.set(xlabel='Position from T1, x (m)',ylabel='Excess temperature θ = T − Tamb (°C)',title=state)
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.savefig(FIG/'phase5_profile_fits.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(8,6),sharex=True,constrained_layout=True)
    for ax,d in zip(axes,models):
        ax.errorbar(X,d['res'],yerr=sd[1:],fmt='o',capsize=3)
        ax.axhline(0,color='black',ls='--');ax.grid(alpha=.25);ax.set(ylabel='Measured − model (°C)',title=d['name'].replace('_',' '))
    axes[-1].set_xlabel('Position from T1, x (m)');fig.suptitle(state);fig.savefig(FIG/'phase5_residuals.png',dpi=180);plt.close(fig)
    notes[3]='# Step 3: Excess-temperature profile\n\n![Profile with error bars](../../docs/figures/module_07/phase5_profile_fits.png)\n\nT1 supplies the boundary excess; TEC A0 is not a rod-profile point. Horizontal bars are conservative position bounds; vertical bars show temporal scatter only. Shared ambient uncertainty is not included because it was not measured.'
    notes[4]='# Step 4: Fit both models\n\nWith θb fixed to measured mean T1 − Tamb, fit one positive parameter m by unweighted least squares to T2–T5. T1 has zero residual by construction. Both fits use the same measured boundary, five positions, and ambient.\n\n$$\\theta_f(x)=\\theta_b\\frac{\\cosh[m(L-x)]}{\\cosh(mL)},\\qquad \\theta_\\infty(x)=\\theta_b e^{-mx}.$$\n\nThe finite solution assumes an insulated tip: dθ/dx at L is zero. Neither fit establishes stationarity or validates this boundary condition.'
    notes[5]='# Step 5: Residuals and fitted m\n\n![Residuals](../../docs/figures/module_07/phase5_residuals.png)\n\n[Residual values](../../data/module_07/phase_5/model_residuals.csv); [parameters](../../data/module_07/phase_5/fit_parameters.csv). Residual = measured minus model.\n\n'
    for d in models:notes[5]+=f'- {d["name"]}: **m = {d["m"]:.4f} ± {d["se"]:.4f} m⁻¹**; T2–T5 RMSE = {d["rmse"]:.4f} °C.\n'
    notes[5]+='\n± values are conditional approximate one-standard-error regression estimates from residual variance and a linearized Jacobian (4 nonbase residuals, 1 parameter, 3 degrees of freedom). They condition on fixed base, ambient, and positions; they are NOT total measurement uncertainties or validated confidence intervals. Nonstationarity, correlated sensor error, and model mismatch limit their interpretation.'
    notes[6]='# Step 6: Characteristic decay length\n\n'
    for d in models:notes[6]+=f'- {d["name"]}: **1/m = {d["length"]:.5f} ± {d["length_se"]:.5f} m**, using δ(1/m) ≈ δm/m².\n'
    mf,ms=models;delta=ms['m']-mf['m'];combined=np.hypot(mf['se'],ms['se'])
    notes[7]=f'# Step 7: Effect of ignoring the finite end\n\nΔm = m_semi − m_finite = **{delta:+.4f} m⁻¹** ({100*delta/mf["m"]:+.1f}% relative to finite m). The magnitude is {abs(delta)/mf["se"]:.2f} times the finite-fit conditional SE and {abs(delta)/ms["se"]:.2f} times the exponential-fit conditional SE. An independence-based SE combination is {combined:.4f} m⁻¹, but the fits share the same data, so this is only a scale comparison, not a significance test. Geometry sensitivity and unknown ambient uncertainty are separate.'
    notes[8]='# Step 8: Systematic errors and tip evidence\n\n- Position error: ruler distances have ±0.001 m bounds, with common-origin correlation. Diameter has a provisional ±0.000025 m bound; confirm caliper accuracy. The fit uses positions/L, not diameter. A 400-draw sensitivity exercise perturbs endpoint readings uniformly within ±0.5 mm and ties T5 to L; it is illustrative, not a measured error distribution.\n'
    for d in models:notes[8]+=f'  - {d["name"]}: position-sensitivity SD in m = {d["position_sensitivity_sd"]:.4f} m⁻¹; changing ambient from 23 to 24 °C gives m = {d["ambient_low"]:.4f} to {d["ambient_high"]:.4f} m⁻¹.\n'
    notes[8]+='- Room drift: no independent ambient time series or ambient uncertainty was saved. The ±0.5 °C exercise is a sensitivity scenario, not an uncertainty measurement. A constant ambient offset changes every excess together.\n- Imperfect contact: unknown hole contact, sensor depth, and conduction along leads can bias individual channels. T3 has downward spikes; no points were silently deleted or calibrated.\n- Tip: a finite model assumes zero axial gradient at the tip, while real end-face convection/radiation may remove heat. The final T4→T5 secant slope is not a measurement of the derivative exactly at L. One tip-adjacent sensor and a changing profile cannot establish an insulated boundary.\n- Thermal drift: the final averaging interval is still evolving, with especially large distal drift. This is a principal unresolved error, not just random scatter.'
    better=min(models,key=lambda d:d['rmse'])
    finite_m=mf['m'];ff=response(finite_m);inf=response(finite_m,finite=False);err=(ff-inf)/ff
    save_csv(DATA/'finite_length_error.csv',['sensor','x_m','relative_error_at_same_finite_fit_m'],[[f'T{i+1}',X[i],err[i]] for i in range(5)])
    notes[9]=f'# Step 9: Compare with predictions and assess adequacy\n\nThe late profile decreases with x, consistent with axial conduction plus side heat loss. Both models are fitted, without assuming a semi-infinite rod. For this provisional interval, **{better["name"].replace("_"," ")}** has the smaller nonbase RMSE. This ranks only the present curve shapes; it is not a validated stationary-model conclusion.\n\nWith finite-fit mL = {finite_m*L:.3f}, the relative difference |θ_f − θ_infinity|/|θ_f| at the same finite-fit m reaches {100*err[-1]:.1f}% at T5. [Sensor-by-sensor errors](../../data/module_07/phase_5/finite_length_error.csv) separate finite-end approximation error from differences between independently fitted m values. The observed tip/base excess ratio is {theta[-1]/theta[0]:.3f}, above 1/e; maximum available separation is documented, not a passed placement test.\n\nThere is no completed quantitative preheating prediction record with a cited k range, so an agreement claim against such a prediction cannot yet be made. Revisit it when available. Constant h, uniform cross-section, negligible radial gradients, negligible radiation, and an insulated tip remain assumptions, not established facts. Radial adequacy requires a separate Biot check; a longitudinal fit alone cannot test it. Unexplained effects include the evolving distal temperatures and sensor-specific spikes.\n\nA fitted m constrains m² = hP/(kA), hence h/k; it cannot independently separate k and h. Units: hP/(kA) is m⁻², m is m⁻¹, and 1/m is m.\n\nThe stationary equation is kA d²T/dx² − hP(T − Tamb) = 0, assuming steady one-dimensional conduction, constant k/h/A/P, no internal generation, and uniform ambient. Boundary conditions are θ(0) = measured θb and dθ/dx(L) = 0 for the finite insulated-tip model; the semi-infinite model replaces the latter by θ→0 as x→∞.'
    for n,text in notes.items():(OUT/f'step_{n}'/'README.md').write_text(text+'\n')
    try:commit=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:commit='Unavailable: no committed checkpoint found.'
    manifest={'raw_csv':str(RAW.relative_to(ROOT)),'raw_sha256':hashlib.sha256(raw_bytes).hexdigest(),'command_csv':str(COMMAND.relative_to(ROOT)),'command_sha256':hashlib.sha256(command_bytes).hexdigest(),'analysis_script':'python/analysis/analyze_phase5.py','analysis_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'repository_HEAD_at_analysis':commit,'note':'HEAD does not establish these inputs or analysis are committed. No commit or push performed.'}
    save_csv(DATA/'provenance.csv',['item','value'],manifest.items())
    lines=['# Module 7: Rod instrument and Phase 5 evidence','',f'**{state}.** These results are a reproducible late-time comparison, not completed stationary validation.','', '## Evidence index','']
    for n in range(1,10):lines.append(f'- [Phase 5 step {n}](../../phase_5/step_{n}/README.md)')
    lines+=['','## Acquisition and sensor map','',f'- [Raw record](../../python/run_data/{RUN}.csv) and [command log](../../python/run_data/{RUN}_commands.csv); originals unchanged.','- A0: TEC base and sole feedback/safety sensor. A1–A5: T1–T5 at x = [0, 0.0275, 0.0500, 0.1000, 0.2050] m. T1 is the rod boundary at x = 0; T5 is the reported tip.','- Material: 6061-T6 aluminum, d = 0.0127 m, L = 0.205 m. Ruler distance bounds ±0.001 m; provisional caliper diameter bound ±0.000025 m. See [repository notes](../../README.md).','- Common-bath completion/pass was reported by the user; quantitative observations and a labeled map photograph are not available in this analysis. No corrections were applied.','- Ambient 23.5 °C is user supplied, without an independently logged time history or uncertainty.','', '## Reproduction and checkpoint','', '`python3 python/analysis/analyze_phase5.py`','',f'Repository HEAD at analysis: `{commit}`. This is not certification that the current acquisition/analysis files are committed. [Input and code hashes](../../data/module_07/phase_5/provenance.csv) identify the exact analyzed contents. No raw data were overwritten.','', '## Outstanding evidence','', '- A qualifying stationary interval (or instructor-approved alternative criterion with justification).','- Quantitative common-bath record, labeled sensor-map photo, and independently measured ambient with uncertainty.','- Completed preheating predictions and exact committed acquisition-code checkpoint.','- Do not present the finite/exponential parameter errors as full uncertainty while thermal drift and ambient error remain unresolved.']
    record=ROOT/'docs/module_notes/module_07_rod_instrument.md';record.write_text('\n'.join(lines)+'\n')
    (ROOT/'docs/module_notes/module_07_stationary_fin.md').write_text('# Stationary-fin analysis\n\nSee the [instrument and analysis record](module_07_rod_instrument.md) and its Phase 5 step links. Results remain provisional because the stationarity criterion is not met.\n')
    assert RAW.read_bytes()==raw_bytes and COMMAND.read_bytes()==command_bytes,'Raw input changed during analysis'
    print(state,'interval',tm[0],tm[-1], 'longest pass',longest)
    for d in models:print(d['name'],'m',d['m'],'SE',d['se'],'RMSE',d['rmse'])
    print('Created phase_5/step_1 through step_9, data/module_07/phase_5, figures, and team notes.')

if __name__=='__main__':main()
