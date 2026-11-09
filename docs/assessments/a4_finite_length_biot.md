# A4: Finite-rod model and validity checks

**Name:** Benjamin Nakash-Kadener  
**Assignment:** A4 - Finite-rod model and validity checks  
**Date:** November 8, 2026  
**Submission filename:** A4_Kadener.pdf

Repository: https://github.com/benkadener/Kadener_Wijnaendts_Module7

**Final Git checkpoint:** `91e797518eef4cf7d2820ec88d9bf684bf35b879`

The calculations use $h=10\,\mathrm{W\,m^{-2}\,K^{-1}}$ and literature conductivity, not experimental temperature-profile fits.

## 1. Fourier's law: Problem 1.3

Assume steady one-dimensional conduction with constant $k$ and no heat generation. Let $x$ increase from the hot side ($x=0$) to the cold side ($x=\ell$).

```math
q_x=-k\frac{dT}{dx}
\quad\Longrightarrow\quad
\int_{T_{\mathrm{hot}}}^{T_{\mathrm{cold}}}dT
=-\frac{q_x}{k}\int_0^\ell dx
```

```math
T_{\mathrm{cold}}-T_{\mathrm{hot}}=-\frac{q_x\ell}{k}
```

```math
\boxed{\Delta T=T_{\mathrm{hot}}-T_{\mathrm{cold}}
=\frac{q_x\ell}{k}=\frac{50\,\mathrm{W\,m^{-1}}}{k}}
```

```math
T_{\mathrm{hot}}=-40\,{}^\circ\mathrm C+\Delta T
\qquad
[\Delta T]=\frac{\mathrm{W\,m^{-1}}}{\mathrm{W\,m^{-1}\,K^{-1}}}=\mathrm K
```

Using the conductivities in Tables A.1-A.2 [1], the final results are:

| Material | $k$ (W/(m·K)) | $\Delta T$ (K) | $T_{\mathrm{hot}}$ (°C) |
|---|---:|---:|---:|
| Pure silver | 427 | $0.117$ | $-39.883$ |
| Pure aluminum | 237 | $0.211$ | $-39.789$ |
| Mild steel, 0.5% carbon | 54 | $0.926$ | $-39.074$ |
| Ice | 2.215 | $22.573$ | $-17.427$ |
| Spruce | 0.11 | $454.545$ | $414.545$ |
| 85% magnesia insulation | 0.067 | $746.269$ | $706.269$ |
| Silica aerogel | 0.024 | $2083.333$ | $2043.333$ |

For example, silver gives $\Delta T=50/427=0.117\,\mathrm K$. Every row uses the same substitution. Metal conductivities are tabulated at 20 °C; the nonmetal values are at 0 °C for ice and aerogel, 20 °C for spruce, and 38 °C for magnesia.

The metals and ice give plausible constant-property estimates; the ice remains frozen. Spruce would decompose at the predicted hot-side temperature. The magnesia result requires a large extrapolation of low-temperature conductivity, so temperature-dependent transport and radiation must be included. The aerogel result is unreasonable for an unchanged material because its structure would degrade at such high temperature and radiation would become important.

## 2. Stationary finite-rod model

Assume a uniform rod, steady state, constant $k$ and $h$, uniform ambient temperature, no internal generation, negligible radial temperature differences, and Newton side cooling. Radiation is neglected in this provisional model. Define $\theta=T-T_\infty$.

### Energy balance and differential equation

A slice of width $\Delta x$ has side area $P\Delta x$. Conservation of energy and Newton cooling give

```math
\dot Q(x)-\dot Q(x+\Delta x)-hP\Delta x\,\theta(x)=0.
```

Divide by $\Delta x$ and take the limit:

```math
-\lim_{\Delta x\to0}\frac{\dot Q(x+\Delta x)-\dot Q(x)}{\Delta x}
-hP\theta=0
\quad\Longrightarrow\quad
\frac{d\dot Q}{dx}=-hP\theta.
```

Fourier's law gives

```math
\dot Q=-kA\frac{dT}{dx}=-kA\frac{d\theta}{dx},
\qquad
\frac{d\dot Q}{dx}=-kA\frac{d^2\theta}{dx^2}.
```

Substitution produces

```math
-kA\frac{d^2\theta}{dx^2}=-hP\theta
\quad\Longrightarrow\quad
\boxed{\frac{d^2\theta}{dx^2}-m^2\theta=0},
\qquad
\boxed{m=\sqrt{\frac{hP}{kA}}}.
```

The slice balance has units W. In the differential balance,

```math
[kA\theta'']=\frac{\mathrm W}{\mathrm{m\,K}}\mathrm{m^2}
\frac{\mathrm K}{\mathrm{m^2}}=\mathrm{W\,m^{-1}},
\qquad
[hP\theta]=\frac{\mathrm W}{\mathrm{m^2\,K}}\mathrm m\,\mathrm K
=\mathrm{W\,m^{-1}}.
```

Thus $[m^2]=\mathrm{m^{-2}}$, $[m]=\mathrm{m^{-1}}$, and $mL$ is dimensionless.

### Boundary conditions and full solution

```math
\theta(0)=\theta_b=T_1-T_\infty,
\qquad
\theta'(L)=0.
```

The first condition sets the temperature at the first rod hole, T1. The second means zero conductive heat flow through the insulated tip. The separate TEC sensor is not the rod-base boundary measurement.

Substitute $\theta=e^{rx}$ into the equation:

```math
(r^2-m^2)e^{rx}=0
\quad\Longrightarrow\quad r=\pm m,
\qquad
\theta=C_1e^{mx}+C_2e^{-mx}.
```

Applying both boundary conditions gives

```math
C_1+C_2=\theta_b,
\qquad
mC_1e^{mL}-mC_2e^{-mL}=0.
```

```math
C_2=C_1e^{2mL},
\qquad
C_1(1+e^{2mL})=\theta_b.
```

```math
C_1=\frac{\theta_b}{1+e^{2mL}}
=\frac{\theta_b e^{-mL}}{2\cosh(mL)},
\qquad
C_2=\frac{\theta_b e^{mL}}{2\cosh(mL)}.
```

```math
\theta(x)=\frac{\theta_b[e^{m(x-L)}+e^{-m(x-L)}]}{2\cosh(mL)}
\quad\Longrightarrow\quad
\boxed{T(x)=T_\infty+\theta_b\frac{\cosh[m(L-x)]}{\cosh(mL)}}.
```

Differentiating gives the tip temperature and base heat rate:

```math
\theta'(x)=-m\theta_b\frac{\sinh[m(L-x)]}{\cosh(mL)},
\qquad
\theta(L)=\frac{\theta_b}{\cosh(mL)}.
```

```math
\dot Q_0=-kA\theta'(0)
=kAm\theta_b\tanh(mL).
```

Here $[kAm\theta_b]=\mathrm W$. The normalized solution equals one at the base, and its derivative is zero at the tip.

### Measured geometry

The rod is reported as 6061-T6 aluminum. The first rod hole defines $x=0$; the analyzed length ends at the tip.

```math
d=(1.2700\pm0.0025)\,\mathrm{cm},
\qquad
L=(20.50\pm0.10)\,\mathrm{cm}.
```

```math
x_{1\ldots5}=(0,\ 2.75,\ 5.00,\ 10.00,\ 20.50)\,\mathrm{cm}.
```

Nonzero position bounds are ±0.10 cm, from a ruler with 1 mm divisions and two endpoint bounds of ±0.5 mm. The caliper's stated measurement error is ±0.025 mm = ±0.0025 cm, used as the diameter uncertainty. T5 and $L$ refer to the same tip location, and shared-origin position errors are correlated.

```math
A=\frac{\pi(0.0127\,\mathrm m)^2}{4}
=1.26677\times10^{-4}\,\mathrm{m^2},
\qquad
P=\pi(0.0127\,\mathrm m)=0.0398982\,\mathrm m.
```

```math
\frac AP=\frac d4=0.003175\,\mathrm m.
```

## 3. Semi-infinite limit and finite-length prediction

### Problem 4.12: semi-infinite limit

This problem uses a prescribed ambient-temperature tip, $\theta(L)=0$, rather than an insulated tip. Start from $\theta=C_1e^{mx}+C_2e^{-mx}$:

```math
C_1+C_2=\theta_b,
\qquad
C_1e^{mL}+C_2e^{-mL}=0
\quad\Longrightarrow\quad C_2=-C_1e^{2mL}.
```

```math
C_1=\frac{\theta_b}{1-e^{2mL}}
=-\frac{\theta_b e^{-mL}}{2\sinh(mL)},
\qquad
C_2=\frac{\theta_b e^{mL}}{2\sinh(mL)}.
```

```math
\frac{\theta(x)}{\theta_b}
=\frac{e^{m(L-x)}-e^{-m(L-x)}}{e^{mL}-e^{-mL}}
=e^{-mx}\frac{1-e^{-2m(L-x)}}{1-e^{-2mL}}.
```

At fixed $x$, both small exponentials vanish as $L\to\infty$:

```math
\lim_{L\to\infty}\frac{\theta(x)}{\theta_b}=e^{-mx},
\qquad
\boxed{T(x)=T_\infty+\theta_b e^{-mx}}.
```

The insulated-tip profile has the same limit:

```math
\frac{\cosh[m(L-x)]}{\cosh(mL)}
=e^{-mx}\frac{1+e^{-2m(L-x)}}{1+e^{-2mL}}
\longrightarrow e^{-mx}.
```

### Literature range and numerical prediction

Table A.1 [1] gives 6061-T6 $k=166$, 167 and 172 W/(m·K) at 0, 20 and 100 °C. Use $k\in[166,172]\,\mathrm{W\,m^{-1}\,K^{-1}}$ as a conservative temperature envelope for planning, not a measured value or statistical confidence interval. Hold $h=10\,\mathrm{W\,m^{-2}\,K^{-1}}$ fixed.

```math
m^2=\frac{hP}{kA}
=\frac{h\pi d}{k\pi d^2/4}=\frac{4h}{kd}.
```

```math
m_{\min}=\sqrt{\frac{4(10)}{172(0.0127)}}=4.279\,\mathrm{m^{-1}},
\qquad
m_{\max}=\sqrt{\frac{4(10)}{166(0.0127)}}=4.356\,\mathrm{m^{-1}}.
```

```math
\boxed{m\in[4.279,4.356]\,\mathrm{m^{-1}}},
\qquad
\boxed{mL\in[0.8772,0.8930]}.
```

```math
\boxed{\frac1m\in[0.2296,0.2337]\,\mathrm m}.
```

Including the diameter and length bounds expands $mL$ to approximately 0.872-0.898. The rod remains shorter than one decay length.

### Finite-length error at each sensor

Compare the two models at the same $m$ and base excess. Define the error relative to the finite-model excess temperature:

```math
\epsilon_T(x)=\frac{|\theta_f(x)-\theta_\infty(x)|}{|\theta_f(x)|}.
```

Since $\theta_f\geq\theta_\infty$ for a positive base excess,

```math
\epsilon_T=1-\frac{\theta_\infty}{\theta_f}
=1-\frac{1+e^{-2mL}}{1+e^{-2m(L-x)}}
=\frac{e^{-2m(L-x)}-e^{-2mL}}{1+e^{-2m(L-x)}}.
```

Choose a maximum local error of **5%**. Both temperature factors and the error are dimensionless. Substituting each measured $x$ and each endpoint of the conductivity range gives:

| Sensor | $x$ (cm) | $100\epsilon_T$, $k=166$ | $100\epsilon_T$, $k=172$ | 5% criterion |
|---|---:|---:|---:|---|
| T1 | 0.00 | $0.000\%$ | $0.000\%$ | Pass |
| T2 | 2.75 | $3.741\%$ | $3.766\%$ | Pass |
| T3 | 5.00 | $7.268\%$ | $7.301\%$ | Fail |
| T4 | 10.00 | $16.634\%$ | $16.639\%$ | Fail |
| T5 | 20.50 | $41.618\%$ | $41.350\%$ | Fail |

For example, $k=166$ gives $m=4.35586\,\mathrm{m^{-1}}$. At T2,

```math
\epsilon_T(0.0275)
=\frac{e^{-2(4.35586)(0.205-0.0275)}-e^{-2(4.35586)(0.205)}}
{1+e^{-2(4.35586)(0.205-0.0275)}}=0.0374127.
```

```math
\boxed{\text{Semi-infinite acceptable at T1-T2; inadequate across T1-T5.}}
```

Retain the finite model for the full measured region. Millimeter-scale geometry bounds do not change these decisions.

### Example 4.8 and Problem 4.20: neglecting tip convection

For a convecting tip, $-kA\theta'(L)=h_{\mathrm{tip}}A\theta(L)$. Write the general solution relative to the tip:

```math
\theta(x)=D\cosh[m(L-x)]+E\sinh[m(L-x)].
```

At $x=L$, $\theta(L)=D$ and $\theta'(L)=-mE$, so

```math
kAmE=h_{\mathrm{tip}}AD
\quad\Longrightarrow\quad
E=\beta D,
\qquad \beta=\frac{h_{\mathrm{tip}}}{km}.
```

The base condition gives

```math
\theta_b=D[\cosh(mL)+\beta\sinh(mL)].
```

Therefore,

```math
\frac{\theta(x)}{\theta_b}
=\frac{\cosh[m(L-x)]+\beta\sinh[m(L-x)]}
{\cosh(mL)+\beta\sinh(mL)}.
```

Differentiating at $x=0$ and using Fourier's law gives

```math
\dot Q_{\mathrm{conv}}
=kAm\theta_b\frac{\sinh(mL)+\beta\cosh(mL)}
{\cosh(mL)+\beta\sinh(mL)}
=kAm\theta_b\frac{\tanh(mL)+\beta}{1+\beta\tanh(mL)}.
```

Example 4.8 uses $d=0.020\,\mathrm m$, $L=0.080\,\mathrm m$, $k=205\,\mathrm{W/(m\,K)}$, $h=h_{\mathrm{tip}}=120\,\mathrm{W/(m^2\,K)}$, and $\theta_b=150-26=124\,\mathrm K$ [1].

```math
A=\frac{\pi(0.020)^2}{4}=3.14159\times10^{-4}\,\mathrm{m^2},
\quad P=\pi(0.020)=0.0628319\,\mathrm m,
```

```math
m=\sqrt{\frac{120(0.0628319)}{205(3.14159\times10^{-4})}}
=10.8200\,\mathrm{m^{-1}},
\quad mL=0.86560,
\quad\beta=\frac{120}{205(10.8200)}=0.05410.
```

```math
T_{\mathrm{tip,conv}}=26+
\frac{124}{\cosh(0.86560)+0.05410\sinh(0.86560)}
=111.43\,{}^\circ\mathrm C,
```

```math
T_{\mathrm{tip,ins}}=26+\frac{124}{\cosh(0.86560)}
=114.66\,{}^\circ\mathrm C.
```

The insulated-tip approximation overpredicts the tip temperature by **3.23 K**. For Problem 4.20,

```math
kAm\theta_b=86.408\,\mathrm W,
```

```math
\dot Q_{\mathrm{conv}}=86.408
\frac{\tanh(0.86560)+0.05410}{1+0.05410\tanh(0.86560)}
=62.713\,\mathrm W,
```

```math
\dot Q_{\mathrm{ins}}=86.408\tanh(0.86560)
=60.411\,\mathrm W.
```

```math
\boxed{100\frac{\dot Q_{\mathrm{conv}}-\dot Q_{\mathrm{ins}}}
{\dot Q_{\mathrm{conv}}}=3.672\%}.
```

For the course rod, provisionally take $h_{\mathrm{tip}}=h$. With $t=\tanh(mL)$, the corresponding relative errors are

```math
\frac{\theta_{\mathrm{tip,ins}}-\theta_{\mathrm{tip,conv}}}
{\theta_{\mathrm{tip,conv}}}
=\frac{\cosh(mL)+\beta\sinh(mL)}{\cosh(mL)}-1
=\beta t,
```

```math
\frac{\dot Q_{\mathrm{conv}}-\dot Q_{\mathrm{ins}}}{\dot Q_{\mathrm{conv}}}
=1-\frac{t(1+\beta t)}{t+\beta}
=\frac{\beta(1-t^2)}{t+\beta}.
```

Here $\beta\in[0.01359,0.01383]$. Substitution gives

```math
\text{Tip-excess error}=0.96\text{-}0.99\%,
\qquad
\text{Base-heat-rate error}=0.94\text{-}0.95\%.
```

Both pass 5% if the real tip convects approximately as assumed. A conducting fixture could invalidate that tip approximation. Small tip-convection error does not remove the much larger finite-length error.

## 4. Transverse Biot number

For a cylinder, use the cross-sectional characteristic length $A/P=d/4=R/2$. The ratio compares radial conduction resistance with surface convection resistance:

```math
\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}
=\frac{h}{k}\frac{\pi d^2/4}{\pi d}
=\frac{hd}{4k}.
```

```math
\mathrm{Bi}_{\perp,\min}=\frac{10(0.0127)}{4(172)}=1.846\times10^{-4},
\qquad
\mathrm{Bi}_{\perp,\max}=\frac{10(0.0127)}{4(166)}=1.913\times10^{-4}.
```

```math
\boxed{\mathrm{Bi}_{\perp}\in[1.846,1.913]\times10^{-4}\ll0.1},
\qquad
[\mathrm{Bi}_{\perp}]
=\frac{(\mathrm{W\,m^{-2}\,K^{-1}})\mathrm m}
{\mathrm{W\,m^{-1}\,K^{-1}}}=1.
```

Including the diameter bounds gives $[1.842,1.916]\times10^{-4}$. Under the alternative radius convention,

```math
\frac{hR}{k}=2\mathrm{Bi}_{\perp}
\in[3.692,3.825]\times10^{-4}.
```

```math
\boxed{\text{Each cross-section may be represented by one temperature.}}
```

This radial conclusion supports a one-dimensional model. It does not justify ignoring the tip: Part 3 requires a finite rod across all five positions.

## Application: still air versus forced airflow

Forced airflow replaces warmed air near the surface more effectively, increasing $h$. At fixed $k$, $A$, and $P$,

```math
\frac1m=\sqrt{\frac{kA}{hP}},
\qquad
\frac{(1/m)_{\mathrm{forced}}}{(1/m)_{\mathrm{still}}}
=\sqrt{\frac{h_{\mathrm{still}}}{h_{\mathrm{forced}}}}.
```

```math
\boxed{h_{\mathrm{forced}}>h_{\mathrm{still}}},
\qquad
\boxed{(1/m)_{\mathrm{forced}}<(1/m)_{\mathrm{still}}}.
```

For example, quadrupling $h$ halves the decay length.