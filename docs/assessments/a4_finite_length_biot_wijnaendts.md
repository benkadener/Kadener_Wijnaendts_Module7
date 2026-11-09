# A4: Finite-Rod Model and Validity Checks

**Name:** [Full name]  
**Assignment:** A4  
**Date:** November 8, 2026  
**Repository URL:** [Repository URL]  
**Exact Git checkpoint:** [Full commit hash of the source checkpoint]

> **Scope:** This version uses textbook properties together with the rod geometry and sensor layout measured in the lab. The heat-transfer coefficient remains the provisional course value, and the conductivity interval is literature-based; the numerical predictions are therefore not a fit to the pilot temperature data.

## 1. Fourier's law — Lienhard Problem 1.3

The slab thickness is $s=1\ \mathrm{cm}=0.010\ \mathrm{m}$, the heat-flux magnitude is $q''=5000\ \mathrm{W\,m^{-2}}$, and the cold-side temperature is $T_c=-40^\circ\mathrm C$. Let $z$ increase from the hot side toward the cold side. For steady, one-dimensional conduction with constant conductivity and no internal generation, Fourier's law gives

$$
q''=-k\frac{dT}{dz}=k\frac{T_h-T_c}{s},
\qquad
\Delta T=T_h-T_c=\frac{q''s}{k}.
$$

The negative sign means heat flows toward decreasing temperature. The units check is

$$
[\Delta T]=\frac{(\mathrm{W\,m^{-2}})(\mathrm m)}{\mathrm{W\,m^{-1}K^{-1}}}=\mathrm K.
$$

A temperature difference of $1\ \mathrm K$ equals a difference of $1^\circ\mathrm C$. Thus every row follows from $\Delta T=(50\ \mathrm{W\,m^{-1}})/k$ and $T_h=-40^\circ\mathrm C+\Delta T$.

| Material | Adopted $k$ ($\mathrm{W\,m^{-1}K^{-1}}$) | $\Delta T$ (K) | $T_h$ ($^\circ\mathrm C$) | Physical assessment |
|---|---:|---:|---:|---|
| Pure silver | 427 | 0.117 | −39.883 | Reasonable; large conductivity produces a small gradient. |
| Pure aluminum | 237 | 0.211 | −39.789 | Reasonable. |
| Mild steel, 0.5% carbon | 54 | 0.926 | −39.074 | Reasonable. |
| Ice | 2.215 | 22.6 | −17.4 | Reasonable as an estimate: the entire slab remains below freezing. |
| Spruce | 0.11 | 455 | 415 | Unreasonable for an unchanged wood slab: thermal decomposition, charring, and possibly combustion invalidate the material model. |
| Insulation, 85% magnesia | 0.067 | 746 | 706 | The constant-property numerical prediction is unreliable: the adopted value is tabulated at $38^\circ\mathrm C$, and $k$ already increases to 0.080 at $204^\circ\mathrm C$. The tabulated data do not support extrapolation over this full span. This alone does not prove that refractory insulation cannot survive the temperature. |
| Silica aerogel | 0.024 | 2083 | 2043 | Unreasonable for intact aerogel with the quoted conductivity: extreme temperatures cause structural changes and strongly increased radiative transfer, and exceed the approximate melting temperature of silica. |

Conductivities are from Lienhard Tables A.1–A.2 [1]: metallic values at $20^\circ\mathrm C$, ice and aerogel at $0^\circ\mathrm C$, spruce at $20^\circ\mathrm C$, and magnesia insulation at $38^\circ\mathrm C$. They give the intended constant-property estimates, including the book's silver result. They are not exact properties at every temperature in the slab. For accurate temperature-dependent conduction, integration instead gives

$$
q''s=\int_{T_c}^{T_h}k(T)\,dT,
$$

whose two sides both have units $\mathrm{W\,m^{-1}}$.

## 2. Derivation of the stationary finite-rod model

### Assumptions, geometry, and energy balance

Take a straight rod of uniform cross-sectional area $A$ and exposed perimeter $P$. The analysis coordinate begins at the first rod thermistor, $x=0$, and ends at the far tip, $x=L$. Assume steady state, no internal heat generation, approximately uniform temperature over each cross-section, constant $k$ and side-convection coefficient $h$, and uniform ambient temperature $T_\infty$. Neglect radiation and heat leaks through supports and sensor wires in this provisional model. Section 4 checks the cross-sectional assumption independently.

Define the excess temperature $\theta(x)=T(x)-T_\infty$. The axial heat rate is

$$
\dot Q(x)=-kA\frac{dT}{dx}=-kA\theta'(x).
$$

For a slice of length $dx$, Newton's law gives the side heat loss $hP\,dx\,\theta$. Conservation of energy at steady state is

$$
\dot Q(x)-\dot Q(x+dx)-hP\theta\,dx=0.
$$

Dividing by $dx$ and taking the limit,

$$
\frac{d\dot Q}{dx}=-hP\theta,
\qquad
kA\frac{d^2\theta}{dx^2}-hP\theta=0.
$$

Therefore the stationary fin equation is

$$
\boxed{\theta''-m^2\theta=0,\qquad m^2=\frac{hP}{kA}.}
$$

The slice balance has units of watts. Both terms of the differential balance have units $\mathrm{W\,m^{-1}}$. In particular,

$$
[m^2]=\frac{(\mathrm{W\,m^{-2}K^{-1}})(\mathrm m)}{(\mathrm{W\,m^{-1}K^{-1}})(\mathrm{m^2})}
=\mathrm{m^{-2}},
$$

so $m$ is an inverse length and $mx$ and $mL$ are dimensionless.

### Boundary conditions and solution

The two boundary conditions are

$$
\theta(0)=\theta_0=T_0-T_\infty,
\qquad
\theta'(L)=0.
$$

The first fixes the temperature at the analysis base, measured by the first rod thermistor. It need not equal the actuator temperature. The second states that no axial heat leaves the insulated tip: $\dot Q(L)=-kA\theta'(L)=0$. An insulated tip can still be warmer than ambient.

The characteristic equation is $r^2-m^2=0$, giving

$$
\theta(x)=C_1e^{mx}+C_2e^{-mx}.
$$

Applying both boundary conditions,

$$
C_1+C_2=\theta_0,
\qquad C_1e^{mL}-C_2e^{-mL}=0,
$$

and hence

$$
C_1=\frac{\theta_0e^{-mL}}{2\cosh(mL)},
\qquad
C_2=\frac{\theta_0e^{mL}}{2\cosh(mL)}.
$$

Substitution yields the finite insulated-tip solution (Lienhard Eq. 4.41):

$$
\boxed{T(x)=T_\infty+(T_0-T_\infty)
\frac{\cosh[m(L-x)]}{\cosh(mL)}.}
$$

For $\theta_0\ne0$, define $\Theta=\theta/\theta_0$. The result obeys $\Theta(0)=1$ and $\Theta'(L)=0$. Fourier's law also gives

$$
\boxed{\dot Q_0=kAm\theta_0\tanh(mL)
=\sqrt{kAhP}\,\theta_0\tanh(mL).}
$$

Here $[kAm\theta_0]=\mathrm W$. As a conservation check, integrating the side loss gives $\int_0^LhP\theta\,dx=(hP/m)\theta_0\tanh(mL)=\dot Q_0$, because $hP/m=kAm$.

## 3. Provisional finite-length prediction

### 3.1 Semi-infinite limit — Problem 4.12

Problem 4.12 specifies a different finite-tip condition: $T(L)=T_\infty$, together with $T(0)=T_0$. Starting with the same exponential general solution, these conditions give

$$
\Theta_L(x)=\frac{\sinh[m(L-x)]}{\sinh(mL)}
=e^{-mx}\frac{1-e^{-2m(L-x)}}{1-e^{-2mL}}.
$$

For fixed $x$ and $m>0$, let $L\to\infty$. Both correction exponentials vanish, so

$$
\boxed{\Theta_\infty(x)=e^{-mx},\qquad
T(x)=T_\infty+\theta_0e^{-mx}.}
$$

Equivalently, bounded temperature tending to ambient at infinity removes the growing exponential. The insulated-tip solution has the same fixed-$x$ limit:

$$
\Theta_{\mathrm{finite}}(x)
=e^{-mx}\frac{1+e^{-2m(L-x)}}{1+e^{-2mL}}
\longrightarrow e^{-mx}.
$$

The decay length is $\ell=1/m$ (meters), and $\dot Q_{0,\infty}=kAm\theta_0$. Taking $L$ large does not guarantee a small *relative* error at sensors that stay close to the tip; the measured region must be checked.

### 3.2 Tip-boundary approximation — Example 4.8 and Problem 4.20

For a convecting tip of area $A$ with coefficient $h_L$, the boundary condition becomes

$$
-kA\theta'(L)=h_LA\theta(L).
$$

Define the dimensionless quantities $a=mL$ and $\beta=h_L/(km)$. The solution and base heat rate are

$$
\Theta_{\mathrm{conv}}(x)=
\frac{\cosh[m(L-x)]+\beta\sinh[m(L-x)]}
{\cosh(a)+\beta\sinh(a)},
$$

$$
\dot Q_{0,\mathrm{conv}}=kAm\theta_0
\frac{\tanh(a)+\beta}{1+\beta\tanh(a)}.
$$

Example 4.8 uses $d=0.020\ \mathrm m$, $L=0.080\ \mathrm m$, $k=205\ \mathrm{W\,m^{-1}K^{-1}}$, $h=h_L=120\ \mathrm{W\,m^{-2}K^{-1}}$, $T_0=150^\circ\mathrm C$, and $T_\infty=26^\circ\mathrm C$. These are the textbook example's inputs, not the course-rod inputs. With $A=\pi d^2/4$ and $P=\pi d$,

$$
m=\sqrt{\frac{4h}{kd}}=10.820\ \mathrm{m^{-1}},
\quad a=0.86560,
\quad \beta=0.05410,
\quad \frac{h_LL}{k}=0.04683.
$$

The insulated-tip prediction is $\Theta_{\mathrm{tip,ins}}=1/\cosh(a)=0.7150$, or $T_{\mathrm{tip,ins}}=114.66^\circ\mathrm C$. Allowing tip convection gives $\Theta_{\mathrm{tip,conv}}=0.6889$, or $T_{\mathrm{tip,conv}}=111.43^\circ\mathrm C$. (The book's intermediate rounded value is 0.6886.) Neglecting tip convection raises the predicted tip temperature by $3.23\ \mathrm K$, about $3.78\%$ of the convecting-tip excess temperature above ambient.

For Problem 4.20,

$$
\dot Q_{0,\mathrm{ins}}=60.41\ \mathrm W,
\qquad \dot Q_{0,\mathrm{conv}}=62.71\ \mathrm W,
$$

$$
\boxed{\frac{\dot Q_{0,\mathrm{conv}}-\dot Q_{0,\mathrm{ins}}}
{\dot Q_{0,\mathrm{conv}}}\times100\%=3.67\%.}
$$

Thus the insulated-tip approximation underpredicts the example's base heat loss by 3.67%, reproducing the textbook answer. This is a comparison of two *finite-tip boundary conditions*, not a test of the semi-infinite approximation. A small tip-convection correction does not establish that the far end can be ignored.

### 3.3 Assumed rod inputs and conductivity range

The course identifies the rod as 6061-T6 aluminum [2]. Lienhard Table A.1 lists $k=166$ at $0^\circ\mathrm C$, $167$ at $20^\circ\mathrm C$, and $172\ \mathrm{W\,m^{-1}K^{-1}}$ at $100^\circ\mathrm C$ [1]. I use

$$
\boxed{k\in[166,172]\ \mathrm{W\,m^{-1}K^{-1}},\qquad
h=10\ \mathrm{W\,m^{-2}K^{-1}}.}
$$

This is a literature-based constant-property bracket for a rod operating approximately within $0$–$100^\circ\mathrm C$, not a statistical confidence interval or a fitted result. If the planned temperatures lie outside this interval, the conductivity bracket must be reconsidered. Pure-aluminum conductivity from Part 1 is inappropriate for this alloy.

For a self-contained numerical example, adopt the following geometry and sensor layout. The diameter is the course's nominal value; the length and positions are illustrative assumptions, not values supplied by the course.

| Model quantity | Adopted value |
|---|---|
| Nominal diameter $d=d_0$ | $0.01270\ \mathrm m$ |
| Measured analysis length $L$: T1 to reported tip position T5 | $0.2050\ \mathrm m$ |
| Measured rod sensor coordinates | $x_1=0$, $x_2=0.0275$, $x_3=0.0500$, $x_4=0.1000$, $x_5=0.2050\ \mathrm m$ |
| Temperature assumption | Normalized errors do not require specific base or ambient temperatures |

The separate actuator thermistor is not one of the five rod-profile positions. The course's nominal $d_0=0.5\ \mathrm{in}=0.01270\ \mathrm m$ gives

$$
A_0=\frac{\pi d_0^2}{4}=1.26677\times10^{-4}\ \mathrm{m^2},
\quad P_0=\pi d_0=0.0398982\ \mathrm m,
\quad \frac{A_0}{P_0}=\frac{d_0}{4}=0.003175\ \mathrm m.
$$

Using this nominal diameter,

$$
\boxed{m\in[4.2792,4.3559]\ \mathrm{m^{-1}},\qquad
1/m\in[0.22958,0.23369]\ \mathrm m.}
$$

The smaller $m$ corresponds to the larger $k$. For the measured $L=0.2050\ \mathrm m$, the dimensionless length range is

$$
\boxed{mL\in[0.8772,0.8930].}
$$

Both endpoints follow by multiplying $m$ in $\mathrm{m^{-1}}$ by $L$ in meters, so the units cancel.

### 3.4 Sensor-by-sensor error and decision criterion

Following the course definition, use relative error in *excess temperature*, with the finite solution as the reference:

$$
\epsilon_T(x)=\frac{|\Theta_{\mathrm{finite}}(x)-e^{-mx}|}
{|\Theta_{\mathrm{finite}}(x)|}.
$$

For $0\le x\le L$, the insulated-tip solution is at least as large as the semi-infinite solution. The exact, dimensionless error simplifies to

$$
\boxed{E(m,L,x)\equiv\epsilon_T(x)=
\frac{e^{-2m(L-x)}-e^{-2mL}}{1+e^{-2m(L-x)}}.}
$$

I choose **$\epsilon_T<0.05$ at every rod sensor used in the analysis, throughout the adopted conductivity range**. This is the course's suggested 5% modeling tolerance; it is not a claim that the thermometer uncertainty is 5%.

For the measured layout, $m_-=4.2792\ \mathrm{m^{-1}}$ and $m_+=4.3559\ \mathrm{m^{-1}}$. Substituting each coordinate and $L=0.2050\ \mathrm m$ into $E$ gives the following completed table. Conductivities in the headings have units $\mathrm{W\,m^{-1}K^{-1}}$.

| Sensor | Position (m) | $\epsilon_T$ at $k=172$ | $\epsilon_T$ at $k=166$ | Largest error over the full $k$ range | Meets 5% criterion? |
|---|---|---|---|---|---|
| Rod 1 | 0.000 | 0.000% | 0.000% | 0.000% | Yes, by base normalization |
| Rod 2 | 0.0275 | 3.766% | 3.741% | 3.766% | Yes |
| Rod 3 | 0.0500 | 7.301% | 7.268% | 7.301% | No |
| Rod 4 | 0.1000 | 16.639% | 16.634% | 16.639% | No |
| Rod 5 | 0.2050 | 41.350% | 41.618% | 41.618% | No |

For example, at rod sensor 3 and $k=172$,

$$
\epsilon_T(0.0500)=\frac{e^{-2(4.279213)(0.2050-0.0500)}-e^{-2(4.279213)(0.2050)}}{1+e^{-2(4.279213)(0.2050-0.0500)}}=0.0730147=7.30147\%.
$$

The error increases with $x$ for fixed $m,L$, so the farthest included sensor is the limiting position. Its dependence on $m$ is not uniform across this measured geometry: the largest errors occur at $k=172$ for Rods 2–4, but at $k=166$ for Rod 5. A numerical sweep of 10,001 points across the interval reproduces these maxima.

Since $e^{-2mL}\ge0$,

$$
\epsilon_T(x)\le\frac{1}{1+e^{2m(L-x)}}
\le\frac{1}{1+e^{2m_-(L-x)}}.
$$

A sufficient condition for all included sensors to pass is therefore

$$
\boxed{m_-(L-x_{\max})>\frac{\ln19}{2}=1.47222.}
$$

For the measured rod, this sufficient condition is not met even at the farthest available sensor because $x_5=L$; the exact table is therefore needed. Rod 2 passes the exact 5% test, while Rods 3–5 fail it. At the tip, $\epsilon_T(L)=(1-e^{-2mL})/2$, which is 41.350–41.618% over the adopted conductivity range.

**Provisional finite-length conclusion for the measured configuration:** Use the finite insulated-tip model over the full sensor region $0\le x\le0.2050\ \mathrm m$. The semi-infinite approximation fails the 5% criterion at $x=0.0500$, $0.1000$, and $0.2050\ \mathrm m$; it is adequate only through $x=0.0275\ \mathrm m$, where the largest error is 3.766%. These conclusions apply to the measured lab layout and the provisional $h$ and $k$ values above.

## 4. Provisional one-dimensional prediction

The transverse characteristic length is $A/P=d/4=R/2$, not the rod's axial length. The course's transverse Biot number is

$$
\boxed{\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}
=\frac{hd}{4k}=\frac{hR}{2k}.}
$$

Its units cancel:

$$
[\mathrm{Bi}_{\perp}]=
\frac{(\mathrm{W\,m^{-2}K^{-1}})(\mathrm m)}{\mathrm{W\,m^{-1}K^{-1}}}=1.
$$

For $h=10\ \mathrm{W\,m^{-2}K^{-1}}$, $k\in[166,172]\ \mathrm{W\,m^{-1}K^{-1}}$, and nominal $d_0=0.01270\ \mathrm m$,

$$
\boxed{\mathrm{Bi}_{\perp}\in[1.8459,1.9127]\times10^{-4}.}
$$

These nominal values are far below unity and below the usual screening threshold of 0.1. Radial conduction can therefore keep a cross-section approximately isothermal while convection removes heat at its surface. A single temperature per cross-section is provisionally well justified for the measured rod under the adopted $h$ and $k$. Local disturbances at contacts and sensor holes are outside this uniform-cylinder estimate.

**Separate radial conclusion:** A small transverse Biot number supports a one-dimensional temperature field $T(x)$; it does not establish the semi-infinite approximation. A rod can be nearly uniform across its radius while still having a temperature profile strongly affected by its far-end boundary. Part 3 tests that separate axial issue.

## 5. Application: still air versus forced airflow

The same heat sink should generally have a larger $h$ in forced airflow because moving air enhances heat exchange with the surface. For unchanged material and fin geometry,

$$
m=\sqrt{\frac{hP}{kA}},\qquad
\ell=\frac1m=\sqrt{\frac{kA}{hP}}.
$$

Thus larger $h$ increases $m$ and decreases the decay length: temperature approaches ambient over a shorter distance along each fin. If airflow raises $h$ by a factor $f$, then $m$ increases by $\sqrt f$ and $\ell$ decreases by $1/\sqrt f$. For example, four times the coefficient halves the decay length. This scaling assumes the one-dimensional fin model remains applicable.

## References and submission checkpoint

1. J. H. Lienhard IV and J. H. Lienhard V, *A Heat Transfer Textbook*, sixth edition, [course-hosted textbook](https://sethfraden.github.io/Phys39F26-course/references/lienhard-heat-transfer-textbook-v6.pdf). Problem 1.3; Section 4.5, especially Eqs. 4.35, 4.41, 4.48–4.50 and Example 4.8; Problems 4.12 and 4.20; Tables A.1–A.2 (printed pp. 739–744).
2. PHYS 39, [Lab 08 and A4 instructions](https://sethfraden.github.io/Phys39F26-course/labs/lab-08/#a4-finite-rod-model-and-validity-checks), accessed November 8, 2026. Source for the course rod's alloy, nominal diameter, coordinate convention, five rod sensors, provisional $h$, and relative-error criterion.

The remaining first-page fields are submission metadata, not experimental inputs. Keep this source at `docs/assessments/a4_finite_length_biot.md`, create and push the source checkpoint, and put its full commit hash and repository URL on the PDF's first page. A commit cannot literally contain its own hash; cite the committed source checkpoint in the exported PDF. Export one PDF named `A4_Lastname.pdf`, keeping the identifying information on page 1. The deadline is November 9, 2026, at 9:05 AM. No Git checkpoint or push has been performed in this non-Git workspace.
