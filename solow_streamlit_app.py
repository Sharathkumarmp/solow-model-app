"""
Solow Growth Model — Interactive Streamlit Simulation
=======================================================

Course   : Economics of Development and Planning (22ECU517A)
Module   : III — Theories of Economic Growth
Author   : Sharath Kumar M P, Assistant Professor, Department of Economics (SF),
           PSG College of Arts and Science, Coimbatore

This app extends the three static matplotlib scripts you shared
(Solow_simulation.py, Solow_simulation_convergance_from_beleow.py,
Solow_simulation_convergance_from_beleow_without_g.py) into a single
interactive tool: every parameter (s, n, g, delta, alpha, initial capital)
is now a slider, and all four charts redraw live.

HOW TO RUN
----------
1. Install dependencies (once):
       pip install streamlit numpy matplotlib pandas
2. Run the app:
       streamlit run solow_streamlit_app.py
3. Your browser will open automatically at http://localhost:8501

To run this from Google Colab instead, see the note at the bottom of this
file — Colab needs a tunnelling step (e.g. via `pyngrok`) to expose the
Streamlit server, or you can adapt the SolowModel class below into a
notebook using ipywidgets (a ready-made version of that is also available
on request).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(page_title="Solow Growth Model — Interactive", layout="wide")

st.markdown(
    """
    <style>
    html, body, [class*="css"]  { font-family: "Times New Roman", serif; }
    .stApp { background-color: #F4F6FB; }
    h1, h2, h3 { color: #1E2761; }
    .metric-box {
        background: #E8EDF8; border: 1px solid #CADCFC; border-radius: 8px;
        padding: 10px 14px; margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("The Solow Growth Model — Interactive Simulation")
st.caption("22ECU517A · Economics of Development and Planning · Module III: Theories of Economic Growth")
st.write(
    "Adjust the parameters in the sidebar and watch capital per effective worker, "
    "output per worker, total output, and living standards converge to (or diverge from) "
    "the steady state — the same mechanics as the three reference scripts, now fully interactive."
)

# ----------------------------------------------------------------------
# Sidebar controls
# ----------------------------------------------------------------------
st.sidebar.header("Model Parameters")

preset = st.sidebar.selectbox(
    "Preset scenario",
    ["Custom (use sliders below)", "Baseline (as in Solow_simulation.py)",
     "Convergence from below (low k0)", "No technological growth (g = 0)"],
)

# Defaults mirror the three uploaded scripts
if preset == "Baseline (as in Solow_simulation.py)":
    d_s, d_n, d_g, d_delta, d_alpha, d_kappa0 = 0.20, 0.01, 0.02, 0.03, 1/3, 8.0
elif preset == "Convergence from below (low k0)":
    d_s, d_n, d_g, d_delta, d_alpha, d_kappa0 = 0.20, 0.01, 0.02, 0.03, 1/3, 1.0
elif preset == "No technological growth (g = 0)":
    d_s, d_n, d_g, d_delta, d_alpha, d_kappa0 = 0.20, 0.01, 0.00, 0.03, 1/3, 1.0
else:
    d_s, d_n, d_g, d_delta, d_alpha, d_kappa0 = 0.20, 0.01, 0.02, 0.03, 1/3, 1.0

s = st.sidebar.slider("Savings rate, s", 0.02, 0.60, d_s, 0.01)
n = st.sidebar.slider("Population growth rate, n", 0.00, 0.05, d_n, 0.001)
g = st.sidebar.slider("Technological growth rate, g", 0.00, 0.05, d_g, 0.001)
delta = st.sidebar.slider("Depreciation rate, δ", 0.00, 0.10, d_delta, 0.005)
alpha = st.sidebar.slider("Capital's output elasticity, α", 0.10, 0.60, d_alpha, 0.01)
kappa_0 = st.sidebar.slider("Initial capital-output ratio, κ₀ = K₀/Y₀", 0.2, 15.0, d_kappa0, 0.1)
T = st.sidebar.slider("Simulation horizon (years)", 50, 400, 200, 10)

st.sidebar.markdown("---")
st.sidebar.caption(
    "κ₀ sets the *initial* capital-output ratio, exactly as in the reference scripts: "
    "k₀ = κ₀^(1/(1−α)). A κ₀ below the steady-state capital-output ratio (s/(n+g+δ)) "
    "produces convergence **from below**; a higher κ₀ produces convergence **from above**."
)

# ----------------------------------------------------------------------
# Simulation (same recurrence as the uploaded scripts)
# ----------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def simulate(s, n, g, delta, alpha, kappa_0, T):
    k_0 = kappa_0 ** (1 / (1 - alpha))
    L_0, E_0 = 1.0, 1.0

    k = np.zeros(T)
    k[0] = k_0
    for t in range(T - 1):
        change_in_k = s * (k[t] ** alpha) - (n + g + delta) * k[t]
        k[t + 1] = max(k[t] + change_in_k, 1e-6)

    y = k ** alpha                      # output per effective worker
    years = np.arange(T)
    L = L_0 * (1 + n) ** years          # labour force
    E = E_0 * (1 + g) ** years          # technology level

    Y = y * E * L                       # total output
    Y_per_person = y * E                # output per person (living standards)

    k_star = (s / (n + g + delta)) ** (1 / (1 - alpha))
    y_star = k_star ** alpha

    df = pd.DataFrame({
        "year": years, "k": k, "y": y, "L": L, "E": E,
        "Y": Y, "Y_per_person": Y_per_person,
    })
    return df, k_star, y_star


df, k_star, y_star = simulate(s, n, g, delta, alpha, kappa_0, T)

# ----------------------------------------------------------------------
# Headline metrics
# ----------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Steady-state k*", f"{k_star:.2f}")
c2.metric("Steady-state y*", f"{y_star:.2f}")
c3.metric("Long-run growth of Y", f"{(n+g)*100:.2f}% / yr")
c4.metric("Long-run growth of Y/L", f"{g*100:.2f}% / yr" if g > 0 else "0.00% / yr (stagnant)")

# ----------------------------------------------------------------------
# 2x2 chart grid — same layout as the reference scripts
# ----------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Solow Growth Model Simulation", fontsize=15, color="#1E2761")

axs[0, 0].plot(df["year"], df["k"], color="#1E2761", linewidth=2)
axs[0, 0].axhline(k_star, color="#8B1A1A", linestyle="--", label=f"Steady state k* ≈ {k_star:.2f}")
axs[0, 0].set_title("Capital per Effective Worker (k)")
axs[0, 0].set_xlabel("Year")
axs[0, 0].grid(True, alpha=0.3)
axs[0, 0].legend()

axs[0, 1].plot(df["year"], df["y"], color="#2D3A8C", linewidth=2)
axs[0, 1].axhline(y_star, color="#8B1A1A", linestyle="--", label=f"Steady state y* ≈ {y_star:.2f}")
axs[0, 1].set_title("Output per Effective Worker (y)")
axs[0, 1].set_xlabel("Year")
axs[0, 1].grid(True, alpha=0.3)
axs[0, 1].legend()

axs[1, 0].plot(df["year"], df["Y"], color="#1A6632", linewidth=2)
axs[1, 0].set_yscale("log")
axs[1, 0].set_title("Total Output (Y) — Log Scale")
axs[1, 0].set_xlabel("Year")
axs[1, 0].grid(True, alpha=0.3)

axs[1, 1].plot(df["year"], df["Y_per_person"], color="#8B1A1A", linewidth=2)
if g == 0:
    axs[1, 1].axhline(y_star, color="#8B1A1A", linestyle="--", label=f"Steady state Y/L ≈ {y_star:.2f}")
    axs[1, 1].legend()
    axs[1, 1].set_title("Output per Person (Y/L) — flattens out when g = 0")
else:
    axs[1, 1].set_yscale("log")
    axs[1, 1].set_title("Output per Person (Y/L) — Log Scale")
axs[1, 1].set_xlabel("Year")
axs[1, 1].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(fig)

# ----------------------------------------------------------------------
# Investment diagram: s*f(k) vs break-even investment
# ----------------------------------------------------------------------
st.subheader("Investment Diagram: Actual vs. Break-Even Investment")
k_max = max(k_star * 2.2, df["k"].iloc[0] * 1.3, 3)
k_grid = np.linspace(0.01, k_max, 200)
invest = s * k_grid ** alpha
breakeven = (n + g + delta) * k_grid

fig2, ax2 = plt.subplots(figsize=(9, 4.5))
ax2.plot(k_grid, invest, color="#1A6632", linewidth=2.2, label="Actual investment  s·f(k)")
ax2.plot(k_grid, breakeven, color="#8B1A1A", linewidth=2.2, label="Break-even investment  (n+g+δ)k")
ax2.scatter([k_star], [(n + g + delta) * k_star], color="#1E2761", zorder=5, label="Steady state k*")
ax2.scatter([df["k"].iloc[0]], [s * df["k"].iloc[0] ** alpha], color="#4B5563", zorder=5, label="Initial k₀")
ax2.set_xlabel("k (capital per effective worker)")
ax2.set_ylabel("Investment per effective worker")
ax2.grid(True, alpha=0.3)
ax2.legend()
st.pyplot(fig2)

# ----------------------------------------------------------------------
# Data table + download
# ----------------------------------------------------------------------
with st.expander("View simulated data table"):
    st.dataframe(df.style.format({"k": "{:.3f}", "y": "{:.3f}", "L": "{:.3f}",
                                   "E": "{:.3f}", "Y": "{:.3f}", "Y_per_person": "{:.3f}"}))

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download simulation data as CSV", csv, "solow_simulation.csv", "text/csv")

st.markdown("---")
st.caption(
    "Model: Y = K^α(AL)^(1−α), with L growing at n and A growing at g. "
    "In per-effective-worker terms, k = K/(AL) evolves as "
    "k(t+1) = k(t) + s·k(t)^α − (n+g+δ)·k(t), converging to "
    "k* = [s/(n+g+δ)]^(1/(1−α))."
)

# ----------------------------------------------------------------------
# NOTE — Running this in Google Colab instead of locally
# ----------------------------------------------------------------------
# Streamlit apps aren't natively rendered inside a Colab notebook cell;
# Colab can only run them via a tunnel. The two common approaches:
#
#   Option A — Colab + pyngrok tunnel (keeps this exact file unchanged):
#       !pip install streamlit pyngrok -q
#       !streamlit run solow_streamlit_app.py &>/content/log.txt &
#       from pyngrok import ngrok
#       print(ngrok.connect(8501))   # click the printed URL
#
#   Option B — a pure-notebook version using ipywidgets + matplotlib,
#       which runs natively in any Colab cell with no tunnelling at all.
#       Ask for the ipywidgets/Colab notebook version if you'd prefer that
#       instead of (or alongside) this Streamlit app.
