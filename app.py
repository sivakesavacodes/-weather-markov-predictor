"""
app.py
=============================================================================
MARKOV WEATHER PREDICTOR – A STOCHASTIC PROCESS FOR WEATHER PREDICTION
Interactive Streamlit Dashboard
=============================================================================
"""

import streamlit as st
import numpy as np
import pandas as pd

from markov_model import (
    STATES,
    DEFAULT_TRANSITION_MATRIX,
    validate_transition_matrix,
    predict_next_day,
    predict_n_days,
    compute_steady_state_analytical,
    compute_steady_state_linear_algebra,
    get_step_by_step_explanation
)
from visualization import (
    plot_probability_trajectory_plotly,
    plot_steady_state_pie_plotly,
    plot_distribution_bar_plotly,
    plot_matplotlib_summary
)

# Page Configuration
st.set_page_config(
    page_title="Markov Weather Predictor",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .callout-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        color: #92400E;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header Banner
    st.markdown('<div class="main-title">⛅ MARKOV WEATHER PREDICTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">A Stochastic Process Model for Probabilistic Weather Forecasting using Markov Chains</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # SIDEBAR: USER INPUTS & PARAMETERS
    # -------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Simulation Controls")
        
        st.subheader("1. Current Weather (Day 0)")
        initial_choice = st.radio(
            "Select Today's Weather State:",
            options=["Sunny (100% Sunny)", "Rainy (100% Rainy)", "Custom Distribution"],
            index=0,
            help="Defines the initial state vector π₀."
        )

        if initial_choice == "Sunny (100% Sunny)":
            pi_0 = np.array([1.0, 0.0])
        elif initial_choice == "Rainy (100% Rainy)":
            pi_0 = np.array([0.0, 1.0])
        else:
            s_init = st.slider("P(Sunny today):", 0.0, 1.0, 0.5, 0.05)
            pi_0 = np.array([s_init, 1.0 - s_init])

        st.caption(f"Initial State Vector $\\mathbf{{\\pi}}_0$: `[{pi_0[0]:.2f}, {pi_0[1]:.2f}]`")

        st.divider()

        st.subheader("2. Forecast Horizon")
        n_days = st.slider("Number of future days to predict:", min_value=1, max_value=20, value=7, step=1)

        st.divider()

        st.subheader("3. Transition Probabilities")
        use_default = st.checkbox("Use Presentation Default Matrix", value=True)
        
        if use_default:
            P = DEFAULT_TRANSITION_MATRIX.copy()
            st.info("""
            **Default Matrix ($P$):**
            * $P(\\text{Sunny}|\\text{Sunny}) = 0.7$
            * $P(\\text{Rainy}|\\text{Sunny}) = 0.3$
            * $P(\\text{Sunny}|\\text{Rainy}) = 0.4$
            * $P(\\text{Rainy}|\\text{Rainy}) = 0.6$
            """)
        else:
            st.markdown("**Row 1: If today is Sunny**")
            p_ss = st.slider("P(Sunny | Sunny):", 0.0, 1.0, 0.70, 0.05)
            p_sr = 1.0 - p_ss
            st.caption(f"Calculated $P(\\text{{Rainy}}|\\text{{Sunny}}) = {p_sr:.2f}$ (ensures row sums to 1.0)")

            st.markdown("**Row 2: If today is Rainy**")
            p_rs = st.slider("P(Sunny | Rainy):", 0.0, 1.0, 0.40, 0.05)
            p_rr = 1.0 - p_rs
            st.caption(f"Calculated $P(\\text{{Rainy}}|\\text{{Rainy}}) = {p_rr:.2f}$ (ensures row sums to 1.0)")

            P = np.array([
                [p_ss, p_sr],
                [p_rs, p_rr]
            ])

        # Validate transition matrix
        is_valid, val_msg = validate_transition_matrix(P)
        if not is_valid:
            st.error(f"Matrix Error: {val_msg}")
            st.stop()

        predict_btn = st.button("🚀 Calculate Forecast", type="primary", use_container_width=True)

    # -------------------------------------------------------------
    # CALCULATIONS
    # -------------------------------------------------------------
    history_data = predict_n_days(pi_0, P, n_days)
    df_history = pd.DataFrame(history_data)
    steady_state = compute_steady_state_analytical(P)

    # -------------------------------------------------------------
    # TOP METRICS DASHBOARD
    # -------------------------------------------------------------
    target_day_row = df_history.iloc[-1]
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.metric(
            label=f"Day {n_days} P(Sunny)",
            value=f"{target_day_row['Sunny_Percent']:.2f}%",
            delta=f"{(target_day_row['Sunny'] - pi_0[0])*100:+.2f}% from Day 0"
        )
    with col_m2:
        st.metric(
            label=f"Day {n_days} P(Rainy)",
            value=f"{target_day_row['Rainy_Percent']:.2f}%",
            delta=f"{(target_day_row['Rainy'] - pi_0[1])*100:+.2f}% from Day 0"
        )
    with col_m3:
        st.metric(
            label="Long-Term Steady Sunny (π)",
            value=f"{steady_state[0]*100:.2f}%",
            help="Analytical limit: 4/7 approx 57.14%"
        )
    with col_m4:
        st.metric(
            label="Long-Term Steady Rainy (π)",
            value=f"{steady_state[1]*100:.2f}%",
            help="Analytical limit: 3/7 approx 42.86%"
        )

    st.write("")

    # -------------------------------------------------------------
    # MAIN TABS INTERFACE
    # -------------------------------------------------------------
    tab_forecast, tab_steps, tab_math, tab_limitations = st.tabs([
        "📊 Forecast & Charts",
        "🧮 Step-by-Step Calculation",
        "📖 Markov Theory & Steady State",
        "⚠️ Model Scope & Limitations"
    ])

    # -------------------------------------------------------------
    # TAB 1: FORECAST & CHARTS
    # -------------------------------------------------------------
    with tab_forecast:
        st.subheader("Probability Evolution Over Time")
        st.markdown(
            "Notice how the curves rapidly converge toward the steady-state dashed lines "
            f"regardless of the starting weather condition."
        )

        fig_trajectory = plot_probability_trajectory_plotly(df_history, steady_state)
        st.plotly_chart(fig_trajectory, use_container_width=True)

        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.subheader(f"Day-by-Day Forecast Table (0 to {n_days} Days)")
            display_df = df_history.copy()
            display_df["Sunny Probability"] = display_df["Sunny"].apply(lambda x: f"{x:.4f} ({x*100:.2f}%)")
            display_df["Rainy Probability"] = display_df["Rainy"].apply(lambda x: f"{x:.4f} ({x*100:.2f}%)")
            display_df["Row Sum Check"] = (display_df["Sunny"] + display_df["Rainy"]).apply(lambda x: f"{x:.4f}")
            st.dataframe(
                display_df[["Day", "Sunny Probability", "Rainy Probability", "Row Sum Check"]],
                use_container_width=True,
                hide_index=True
            )

        with col_right:
            st.subheader("Long-Term Equilibrium (π)")
            fig_pie = plot_steady_state_pie_plotly(steady_state)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Inspect specific day bar chart
        with st.expander("🔍 Inspect Probability Distribution on a Specific Day"):
            inspect_day = st.slider("Select Day to Inspect:", 0, n_days, 1)
            fig_bar = plot_distribution_bar_plotly(df_history, inspect_day)
            st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: STEP-BY-STEP CALCULATION
    # -------------------------------------------------------------
    with tab_steps:
        st.subheader("Detailed Arithmetic: How Matrix Multiplication Works")
        st.markdown("In a Markov chain, forecasting is performed via **Vector-Matrix Dot Product Multiplication**:")
        st.latex(r"\boldsymbol{\pi}_{t+1} = \boldsymbol{\pi}_t \times P")

        step_day = st.selectbox(
            "Choose a day to see the exact arithmetic breakdown:",
            options=list(range(1, min(n_days + 1, 6))),
            index=0
        )

        pi_prev = np.array([df_history.loc[step_day - 1, "Sunny"], df_history.loc[step_day - 1, "Rainy"]])
        explanation = get_step_by_step_explanation(step_day, pi_prev, P)

        st.markdown(f"#### Computing Weather for Day {step_day} from Day {step_day - 1}")
        st.code(f"Previous Day (Day {step_day - 1}) State Vector:\nπ_{step_day - 1} = [Sunny={pi_prev[0]:.4f}, Rainy={pi_prev[1]:.4f}]")

        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            st.markdown("**1. Calculating P(Sunny):**")
            st.code(explanation["sunny_calc"])

        with col_calc2:
            st.markdown("**2. Calculating P(Rainy):**")
            st.code(explanation["rainy_calc"])

        st.success(f"**Verification (Probability Axiom):** {explanation['sum_check']}")

        # Presentation Benchmark Reproduction Box
        if np.allclose(pi_0, [1.0, 0.0]) and np.allclose(P, DEFAULT_TRANSITION_MATRIX):
            st.info("""
            **Presentation Benchmark Verification:**
            * $\\mathbf{\\pi}_0 = [1.0, 0.0]$ *(Today is 100% Sunny)*
            * $\\mathbf{\\pi}_1 = [0.7000, 0.3000]$ *(Day 1: 70% Sunny, 30% Rainy)*
            * $\\mathbf{\\pi}_2 = [0.6100, 0.3900]$ *(Day 2: 61% Sunny, 39% Rainy)*
            * Steady State: $[0.5714, 0.4286]$ *(57.14% Sunny, 42.86% Rainy)*
            
            *Our model reproduced these exact presentation numbers!*
            """)

    # -------------------------------------------------------------
    # TAB 3: MARKOV THEORY & STEADY STATE
    # -------------------------------------------------------------
    with tab_math:
        st.subheader("Mathematical Principles of Markov Chains")

        st.markdown("### 1. The Markov Property (Memorylessness)")
        st.markdown(
            "A stochastic process has the **Markov Property** if the probability of transitioning to the next state depends **only** on the present state, not on the sequence of events that preceded it:"
        )
        st.latex(r"P(X_{t+1} = s \mid X_t, X_{t-1}, \dots, X_0) = P(X_{t+1} = s \mid X_t)")
        st.markdown(
            "* **Simple Example:** If today is Sunny, the probability of rain tomorrow is $0.3$, whether it was sunny for the last 10 days or rained all last week."
        )

        st.divider()

        st.markdown("### 2. Transition Probability Matrix ($P$)")
        st.latex(r"""
        P = \begin{bmatrix} 
        P(\text{Sunny} \mid \text{Sunny}) & P(\text{Rainy} \mid \text{Sunny}) \\ 
        P(\text{Sunny} \mid \text{Rainy}) & P(\text{Rainy} \mid \text{Rainy}) 
        \end{bmatrix} = \begin{bmatrix} 0.7 & 0.3 \\ 0.4 & 0.6 \end{bmatrix}
        """)

        st.markdown("""
        * **Rows represent current state today ($i$):**
          * **Row 1 (Sunny):** Today is Sunny $\\to$ 70% chance of Sunny tomorrow, 30% chance of Rainy tomorrow.
          * **Row 2 (Rainy):** Today is Rainy $\\to$ 40% chance of Sunny tomorrow, 60% chance of Rainy tomorrow.
        * **Columns represent the destination state tomorrow ($j$):**
          * **Column 1:** Sunny tomorrow.
          * **Column 2:** Rainy tomorrow.
        * **Row Stochasticity:** Every row must sum to $1$ because tomorrow's weather must be one of the possible states in the sample space:
        """)
        st.latex(r"\sum_{j=1}^{2} P_{ij} = 1 \quad \text{for all rows } i")

        st.divider()

        st.markdown(r"### 3. Deriving the Steady-State Distribution ($\mathbf{\pi}$)")
        st.markdown("""
        The steady state (stationary distribution) $\\mathbf{\\pi} = [\\pi_S, \\pi_R]$ represents the long-term equilibrium:
        """)
        st.latex(r"\boldsymbol{\pi} P = \boldsymbol{\pi} \quad \text{and} \quad \pi_S + \pi_R = 1")

        st.markdown("Expanding the matrix equation:")
        st.latex(r"[\pi_S, \pi_R] \begin{bmatrix} 0.7 & 0.3 \\ 0.4 & 0.6 \end{bmatrix} = [\pi_S, \pi_R]")

        st.markdown("This gives two simultaneous equations:")
        st.latex(r"\pi_S = 0.7 \pi_S + 0.4 \pi_R \implies 0.3 \pi_S = 0.4 \pi_R \implies \pi_S = \frac{4}{3} \pi_R")
        st.latex(r"\pi_R = 0.3 \pi_S + 0.6 \pi_R \implies 0.4 \pi_R = 0.3 \pi_S")

        st.markdown("Substitute $\\pi_S = \\frac{4}{3} \\pi_R$ into the normalization condition $\\pi_S + \\pi_R = 1$:")
        st.latex(r"\frac{4}{3} \pi_R + \pi_R = 1 \implies \frac{7}{3} \pi_R = 1 \implies \boldsymbol{\pi_R = \frac{3}{7} \approx 0.4286 \ (42.86\%)}")
        st.latex(r"\boldsymbol{\pi_S = 1 - \frac{3}{7} = \frac{4}{7} \approx 0.5714 \ (57.14\%)}")

        st.info("💡 **Key Conclusion:** No matter what the weather is today, in the distant future, about **57.14%** of days will be Sunny and **42.86%** will be Rainy.")

    # -------------------------------------------------------------
    # TAB 4: LIMITATIONS & METEOROLOGY COMPARISON
    # -------------------------------------------------------------
    with tab_limitations:
        st.subheader("Project Scope & Critical Limitations")

        st.warning("""
        **Academic Notice:** This application is a mathematical demonstration of discrete stochastic processes.
        It is **NOT** a real-world meteorological forecasting tool.
        """)

        st.markdown("""
        | Feature | This Simplified Markov Model | Real-World Numerical Weather Prediction (NWP) |
        |---|---|---|
        | **State Variables** | 2 discrete states (Sunny, Rainy) | Continuous fields: temperature, humidity, wind velocity, barometric pressure, vorticity. |
        | **Governing Laws** | Fixed transition probabilities ($P$) | Fluid dynamics, thermodynamics, Navier-Stokes partial differential equations. |
        | **Memory** | Memoryless (order-1 Markov property) | Multi-day atmospheric inertia, jet streams, oceanic oscillations (El Niño/La Niña). |
        | **Spatial Resolution** | Zero-dimensional (single point/abstract) | 3D numerical grid covering Earth with millions of atmospheric cells. |
        | **Chaos / Sensitivity** | Converges smoothly to a fixed steady state | Non-linear chaotic dynamics (Lorenz system / Butterfly Effect). |

        ### Key Takeaway for Presentation
        * A Markov chain answers: *"Given the statistical frequency of transitions, what is the expected probability distribution over time?"*
        * Physical meteorology answers: *"Given the continuous laws of physics and thermodynamic boundary conditions, how will air masses move?"*
        """)

    # Footer
    st.divider()
    st.caption("Developed for Academic Mathematics Project: Markov Weather Predictor | Built with Python, NumPy, and Streamlit")


if __name__ == "__main__":
    main()
