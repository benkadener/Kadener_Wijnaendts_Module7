from pathlib import Path
from math import pi,sqrt,cosh,sinh,tanh,exp
import html,re,csv
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / 'output' / 'pdf'
ROOT.mkdir(parents=True, exist_ok=True)
SOURCE = REPO / 'docs' / 'assessments'
SOURCE.mkdir(parents=True, exist_ok=True)
checkpoint='91e797518eef4cf7d2820ec88d9bf684bf35b879'
xs=[0,.0275,.05,.1,.205];ks=[166,172];d=.0127;L=.205;h=10
rows=[]
for i,x in enumerate(xs,1):
 vals=[]
 for k in ks:
  m=sqrt(4*h/k/d);f=cosh(m*(L-x))/cosh(m*L);e=exp(-m*x);vals.append(100*(f-e)/f)
 rows.append(f'| T{i} | {100*x:.2f} | {vals[0]:.3f} | {vals[1]:.3f} | '+('Pass' if max(vals)<=5 else 'Fail')+' |')
text='''# A4: Finite-rod model and validity checks

Benjamin Nakash-Kadener | November 8, 2026 | Individual assignment

Repository: https://github.com/benkadener/Kadener_Wijnaendts_Module7

Geometry checkpoint: `91e797518eef4cf7d2820ec88d9bf684bf35b879`

This checkpoint identifies the measured geometry used below. This newly prepared assessment is a review draft; its final source and PDF must be committed and the cited checkpoint pushed before submission. These are provisional predictions using h = 10 W/(m^2 K), not fits to experimental temperatures.

## 1. Fourier's law: Lienhard Problem 1.3

For a uniform slab of thickness ell = 0.010 m, assume steady one-dimensional conduction, no internal generation, and constant k. Choose x from hot to cold. Fourier's law q_x = -k dT/dx gives the positive temperature rise from cold to hot:

    Delta T = |q_x| ell/k = (5000 W/m^2)(0.010 m)/k = (50 W/m)/k
    T_hot = -40 deg C + Delta T

The units are (W/m)/(W/(m K)) = K; temperature differences in K and degrees C have equal numerical values. Table A.1 supplies the metallic values at 20 deg C; Table A.2 supplies the nonmetallic values at their listed reference temperatures. Values are constant-property estimates, not evaluations of k at every temperature through the slab. [1, Tables A.1-A.2, printed pp. 739-744]

| Material | k, W/(m K) | Delta T, K | T_hot, deg C |
|---|---:|---:|---:|
'''
for name,k in [('Pure silver',427),('Pure aluminum',237),('Mild steel, 0.5% C',54),('Ice (0 deg C property)',2.215),('Spruce (20 deg C property)',.11),('85% magnesia (38 deg C property)',.067),('Silica aerogel (0 deg C property)',.024)]:
 text+=f'| {name} | {k:g} | {50/k:.3f} | {-40+50/k:.3f} |\n'
text+='''
The silver result, 0.117 K, reproduces the supplied check. Metal temperatures and the ice result are physically plausible within this approximate calculation; the ice stays below freezing, although its conductivity varies with temperature. The spruce result is unreasonable for an unchanged solid slab because wood decomposes at such temperatures. The magnesia and aerogel predictions extrapolate low-temperature conductivities through enormous temperature ranges: temperature-dependent conduction and radiation cannot be neglected. The aerogel result also exceeds the range in which its original silica structure can remain unchanged. These extreme numbers invalidate the constant-property model; they are not reliable operating temperatures.

---PAGE---
## 2. Derivation of the finite insulated-tip model

Consider a uniform rod with cross-sectional area A and perimeter P. Define excess temperature theta(x) = T(x) - T_infinity, where T_infinity is uniform room temperature. The stationary slice balance is conduction in minus conduction out minus side convection = 0:

    Q(x) - Q(x+dx) - h P dx theta = 0
    Q(x) = -k A dT/dx
    dQ/dx = -h P theta
    k A d^2 theta/dx^2 - h P theta = 0
    theta'' - m^2 theta = 0,       m = sqrt(hP/(kA))

The first balance has units W. After division by dx, kA theta'' and hP theta each have units W/m. Also [hP/(kA)] = m^-2, so m is in m^-1 and mL is dimensionless. [1, Section 4.5, Eqs. 4.28-4.35]

Assumptions: steady state; constant k, h, A and P; no internal heat generation; negligible temperature variation across each cross-section; and side loss described by Newton cooling to a uniform environment. Radiation is omitted from the provisional h. The following tip condition is an approximation for a real exposed end, checked separately in Part 3.

The two boundary conditions are theta(0) = theta_b and theta'(L) = 0. The first prescribes the rod-base temperature; the second sets the conductive heat flow through the tip to zero. In this apparatus T1 at the first hole defines x = 0 and supplies theta_b. The TEC thermistor A0 and the requested TEC setpoint do not supply the rod boundary temperature.

Write the general solution and apply both conditions:

    theta = C1 exp(mx) + C2 exp(-mx)
    C1 + C2 = theta_b
    C1 exp(mL) - C2 exp(-mL) = 0
    C1 = theta_b exp(-mL)/(2 cosh(mL))
    C2 = theta_b exp(mL)/(2 cosh(mL))

Substitution yields the finite insulated-tip result:

    theta(x)/theta_b = cosh[m(L-x)]/cosh(mL)
    theta(L)/theta_b = 1/cosh(mL)
    Q_base = k A m theta_b tanh(mL)

It is exactly one at x = 0 and its derivative vanishes at x = L. Since kAm has units W/K, the base heat rate has units W. This follows the derivation in Section 4.5 rather than assuming an exponential profile. [1, Eqs. 4.36-4.45]

## Measured geometry used for the predictions

The reported material is 6061-T6 aluminum. The analysis length from T1 to the tip is L = (20.50 +/- 0.10) cm; d = (1.2700 +/- 0.0025) cm. Positions T1-T5 are 0, 2.75, 5.00, 10.00 and 20.50 cm relative to T1, with +/- 0.10 cm bounds on measured nonzero distances. T5 is the reported tip location. The ruler has 1 mm divisions; conservative two-endpoint distance bounds are +/- 1 mm. The caliper's reported 0.025 mm specification is used provisionally as a diameter bound; its status as accuracy rather than resolution remains to be confirmed.

    A = pi d^2/4 = 1.26677e-4 m^2
    P = pi d = 0.0398982 m
    A/P = d/4 = 0.003175 m;     P L = 0.00817914 m^2

T1 defines the origin. Shared-origin errors are correlated, and T5 and L refer to the same endpoint. Extra digits above describe calculation precision, not measurement accuracy.

---PAGE---
## 3. Semi-infinite limit and finite-length prediction

Problem 4.12 specifies theta(0) = theta_b and theta(L) = 0. Those conditions applied to the exponential general solution give a finite prescribed-ambient-tip profile:

    theta/theta_b = sinh[m(L-x)]/sinh(mL)
    = exp(-mx) [1-exp(-2m(L-x))]/[1-exp(-2mL)]

At fixed x as L tends to infinity, both small exponentials vanish and theta/theta_b tends to exp(-mx), Eq. 4.50. The insulated-tip solution has plus signs instead of minus signs in this expression and reaches the same limit. A fixed-temperature tip and an insulated tip are different finite problems, although their long-rod limits agree. [1, Problem 4.12, printed p. 186]

### Conductivity range and dimensionless length

Table A.1 gives 6061-T6 conductivity 167 W/(m K) at 20 deg C, 166 at 0 deg C, and 172 at 100 deg C. Use k = 166-172 W/(m K), a conservative tabulated temperature envelope bracketing room temperature through the planned heating range. This is a literature/planning envelope, not a measured conductivity or a statistical confidence interval. The assigned h is fixed at 10 W/(m^2 K); its real uncertainty is not determined here. [1, Table A.1, printed p. 739]

    m = sqrt(4h/(kd)) = 4.279-4.356 m^-1
    mL = 0.8772-0.8930
    1/m = 0.2296-0.2337 m
    Bi_parallel = (mL)^2 = 0.7695-0.7974

The length is less than one decay length. A large-mL assumption is therefore not established. Retaining the measured diameter and length bounds expands m to approximately 4.275-4.360 m^-1 and mL to 0.872-0.898; the conclusion is unchanged.

### Error at every planned sensor

Compare finite and semi-infinite excess temperatures at the same k, h, geometry and base excess. Define the relative error using the finite solution in the denominator; this is error in excess temperature, not in absolute Celsius temperature:

    epsilon_T(x) = |theta_finite - theta_infinite|/|theta_finite|
    = [exp(-2m(L-x)) - exp(-2mL)]/[1+exp(-2m(L-x))]

Adopt a 5% maximum local error tolerance at each retained position. This is an explicit analysis choice. The following values use nominal measured geometry; all are percentages.

| Sensor | x, cm | Error at k=166 | Error at k=172 | 5% decision |
|---|---:|---:|---:|---|
'''+ '\n'.join(rows)+'''

T1 and T2 meet this tolerance, but T3-T5 do not. The semi-infinite approximation is inadequate across the full planned measured region under this parameter envelope; retain the finite insulated-tip model. At the tip the error is about 41.4-41.6%. The interval ends of k alone are not statistical error bars. Millimeter-scale geometry bounds do not change any pass/fail decision.

---PAGE---
### Tip-boundary approximation: Example 4.8 and Problem 4.20

For a convecting tip, the boundary balance is -kA theta'(L) = h_tip A theta(L). Define beta = h_tip/(km). The exact solution and base heat rate are:

    theta/theta_b = [cosh(m(L-x)) + beta sinh(m(L-x))]
                     / [cosh(mL) + beta sinh(mL)]
    Q_conv = kAm theta_b [beta+tanh(mL)]/[1+beta tanh(mL)]

Example 4.8 uses d = 0.020 m, L = 0.080 m, k = 205 W/(m K), h = h_tip = 120 W/(m^2 K), base 150 deg C and ambient 26 deg C. Thus mL = 0.86560 and beta = 0.05410. The exact tip temperature is 111.43 deg C; an insulated tip gives 114.66 deg C, an overestimate of 3.23 K. [1, Example 4.8, printed p. 172]

For Problem 4.20, the corresponding heat rates are Q_conv = 62.713 W and Q_insulated = 60.411 W. Neglecting tip convection underestimates the exact base heat rate by

    100 (Q_conv - Q_insulated)/Q_conv = 3.672%

This reproduces the textbook check of 3.67%. Small radial Biot number does not, by itself, mean zero tip heat loss. [1, Problem 4.20, printed p. 187]

For the course geometry, assuming provisionally h_tip = h = 10 W/(m^2 K), beta = 0.01359-0.01383. Relative to the convecting-tip model, an insulated tip overpredicts tip excess by beta tanh(mL), about 0.96-0.99%, and underpredicts base heat flow by about 0.94-0.95%. This supports the insulated-tip approximation at a 5% planning tolerance if the actual tip exchanges heat approximately this way. A fixture or other tip contact could invalidate that estimate. A justified insulated tip does not justify an infinite rod: its finite-length temperature error above remains large.

## 4. Transverse Biot-number prediction

For a circular rod the cross-sectional conduction-to-convection resistance ratio uses characteristic length A/P = d/4 = R/2:

    Bi_perp = h(A/P)/k = hd/(4k)
    = 1.846e-4 to 1.913e-4

The ratio is dimensionless because (W/(m^2 K)) m / (W/(m K)) = 1. It is far below 0.1, supporting a single temperature for each cross-section under these conditions. With diameter bounds the range is approximately 1.842e-4 to 1.916e-4. The radius-based convention hR/k is twice as large, 3.692e-4 to 3.825e-4, and reaches the same radial conclusion. This does not make the whole rod isothermal: axial gradients remain essential. [1, Eq. 4.27; 2]

The conclusions are separate: negligible radial variation supports a one-dimensional finite-rod model, whereas the approximately 42% tip-region infinite-rod error rejects the semi-infinite approximation over all five positions.

### Application: still air versus forced airflow

Forced airflow generally increases h for the same heat sink and geometry by replacing warmed fluid near its surface more effectively. Since 1/m = sqrt(kA/(hP)), a larger h shortens the axial decay length; for example, quadrupling h halves 1/m at fixed k and geometry. The temperature approaches ambient over a shorter distance. The radial Biot number increases with h and must be checked again.

## References and review status

[1] J. H. Lienhard IV and J. H. Lienhard V, A Heat Transfer Textbook, version 6, Section 4.5; Problems 1.3, 4.12 and 4.20; Example 4.8; Appendix A, Tables A.1-A.2. Page references above use printed textbook pages.
https://sethfraden.github.io/Phys39F26-course/references/lienhard-heat-transfer-textbook-v6.pdf

[2] Module 7, Part II: Finite and Infinite Rod Theory, course reference, accessed November 8, 2026.
https://sethfraden.github.io/Phys39F26-course/labs/fin-design-derivation/

[3] A4 assignment requirements, accessed November 8, 2026.
https://sethfraden.github.io/Phys39F26-course/labs/lab-08/#a4-finite-rod-model-and-validity-checks

Review before individual submission: check the derivations in your own words, confirm the caliper specification and tip sensor location, and commit/push the finished assessment. The hash on page 1 identifies the existing geometry checkpoint, not an uncreated final assessment commit. No Part III temperature-profile data are needed for these A4 predictions.
'''
(SOURCE/'a4_finite_length_biot.md').write_text(text)
styles=getSampleStyleSheet();styles['Normal'].fontSize=9;styles['Normal'].leading=12;styles['Normal'].spaceAfter=5
styles.add(ParagraphStyle(name='Equation',fontName='Courier',fontSize=8,leading=11,spaceAfter=7))
styles['Heading1'].fontSize=18;styles['Heading1'].leading=22
styles['Heading2'].fontSize=13;styles['Heading2'].leading=16
styles['Heading3'].fontSize=11;styles['Heading3'].leading=14
story=[];lines=text.splitlines();i=0
while i<len(lines):
 line=lines[i]
 if not line: i+=1;continue
 if line=='---PAGE---':story.append(PageBreak());i+=1;continue
 if line.startswith('|'):
  data=[]
  while i<len(lines) and lines[i].startswith('|'):
   parts=[s.strip() for s in lines[i].strip('|').split('|')]
   if not all(re.fullmatch(r'[-:]+',s) for s in parts):data.append([Paragraph(html.escape(s),styles['Normal']) for s in parts])
   i+=1
  t=Table(data,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,colors.grey),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4)]));story.extend([t,Spacer(1,9)]);continue
 if line.startswith('    '):
  block=[]
  while i<len(lines) and lines[i].startswith('    '):block.append(lines[i][4:]);i+=1
  story.append(Preformatted('\n'.join(block),styles['Equation']));continue
 level=len(line)-len(line.lstrip('#'))
 if level:story.append(Paragraph(html.escape(line[level:].strip()),styles['Heading'+str(min(level,3))]));i+=1;continue
 para=[]
 while i<len(lines) and lines[i] and not lines[i].startswith(('#','|','    ','---PAGE---')):para.append(lines[i]);i+=1
 val=html.escape(' '.join(para).replace('`',''))
 val=re.sub(r'(https://[^\s]+)',r'<link href="\1" color="#235784">\1</link>',val)
 story.append(Paragraph(val,styles['Normal']))
def footer(c,doc):
 c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(43,24,'Benjamin Nakash-Kadener | A4 | Review draft');c.drawRightString(569,24,str(doc.page))
SimpleDocTemplate(str(ROOT/'A4_Kadener.pdf'),pagesize=(612,792),rightMargin=43,leftMargin=43,topMargin=37,bottomMargin=38,title='A4: Finite-rod model and validity checks',author='Benjamin Nakash-Kadener').build(story,onFirstPage=footer,onLaterPages=footer)
print(ROOT)
