# Solow Growth Model — Interactive Simulation

An interactive Streamlit app for exploring the Solow-Swan neoclassical growth model.
Adjust the savings rate (s), population growth rate (n), technological growth rate (g),
depreciation rate (δ), and capital's output elasticity (α) with live sliders, and watch
capital per worker, output per worker, total output, and living standards converge to
(or diverge from) the steady state in real time.

Built for Module III (Theories of Economic Growth), 22ECU517A — Economics of
Development and Planning.

## Features
- Live sliders for all five model parameters
- Preset scenarios (baseline, high savings, fast population growth, no tech growth)
- Steady-state metrics (k*, y*, long-run growth rates)
- Investment diagram: actual vs. break-even investment
- Downloadable simulation data (CSV)

## Run locally
\`\`\`
pip install -r requirements.txt
streamlit run solow_streamlit_app.py
\`\`\`
