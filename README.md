# Solow Growth Model — Interactive Simulation

An interactive Streamlit app for exploring the Solow-Swan neoclassical growth model.
Adjust the savings rate (s), population growth rate (n), technological growth rate (g),
depreciation rate (δ), and capital's output elasticity (α) with live sliders, and watch
capital per worker, output per worker, total output, and living standards converge to
(or diverge from) the steady state in real time.

Built for Understanding Theories of Economic Growth

## Features

- Live sliders for all five model parameters (s, n, g, δ, α) plus initial capital
- Preset scenarios: baseline, high savings, fast population growth, no technological growth
- Steady-state metrics: k*, y*, long-run growth of Y, long-run growth of Y/L
- Four-panel chart grid: capital per effective worker, output per effective worker,
  total output (log scale), output per person
- Investment diagram: actual investment s·f(k) vs. break-even investment (n+g+δ)k,
  with markers for the current k and the steady-state k*
- Simulated data table with CSV download

## Run locally

```bash
pip install -r requirements.txt
streamlit run solow_streamlit_app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## The model

Output is produced according to Y = K^α(AL)^(1−α), with the labour force L growing at
rate n and technology A growing at rate g. In per-effective-worker terms, with
k = K/(AL), the economy's capital-labour ratio evolves according to:

```
k(t+1) = k(t) + s·k(t)^α − (n + g + δ)·k(t)
```

which converges to the steady state:

```
k* = [s / (n + g + δ)]^(1 / (1 − α))
```

## File structure

```
.
├── solow_streamlit_app.py   # the Streamlit app
├── requirements.txt         # Python dependencies
└── README.md                 # this file
```

## Author

Sharath Kumar M P
Assistant Professor and Head i/c, Department of Economics (SF)
PSG College of Arts and Science, Coimbatore
