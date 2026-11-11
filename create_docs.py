"""
create_docs.py
Expanded and comprehensive generator for:
1. PowerPoint Presentation (17 in-depth academic slides)
2. Word Document Report (Comprehensive academic thesis/project report)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

import docx
from docx import Document
from docx.shared import Inches as DocxInches, Pt as DocxPt, RGBColor as DocxRGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


# -----------------------------------------------------------------------------
# 1. GENERATE EXPANDED POWERPOINT PRESENTATION (17 SLIDES)
# -----------------------------------------------------------------------------
def build_powerpoint(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    DARK_BLUE = RGBColor(30, 58, 138)
    LIGHT_BG = RGBColor(248, 250, 252)
    TEXT_DARK = RGBColor(31, 41, 55)
    AMBER = RGBColor(245, 158, 11)
    OCEAN_BLUE = RGBColor(59, 130, 246)
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(16, 185, 129)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="MARKOV WEATHER PREDICTOR | ACADEMIC PROJECT"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = OCEAN_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE

    def add_card(slide, left, top, width, height, title, points, bg_color=WHITE, border_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(15)
            p_title.font.bold = True
            p_title.font.color.rgb = DARK_BLUE
            p_title.space_after = Pt(8)
            first_bullet = True
        else:
            first_bullet = False

        for pt in points:
            p = tf.add_paragraph() if (title or not first_bullet) else tf.paragraphs[0]
            first_bullet = False
            p.text = f"•  {pt}"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(5)

    # ---------------- SLIDE 1: TITLE SLIDE ----------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "APPLIED MATHEMATICS & STOCHASTIC PROCESSES"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = AMBER
    p_badge.space_after = Pt(14)

    p_main = tf1.add_paragraph()
    p_main.text = "MARKOV WEATHER PREDICTOR"
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Discrete-Time Stochastic Process Model for Weather Prediction & Convergence Analysis"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = RGBColor(209, 213, 219)
    p_sub.space_after = Pt(28)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Author: Siva Kesava | GitHub: sivakesavacodes\nLive Web Dashboard: https://5frtkkawtnf5aazokkb8ar.streamlit.app/"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(156, 163, 175)

    # ---------------- SLIDE 2: MOTIVATION & PROBLEM STATEMENT ----------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Motivation: Why Model Weather Stochastically?")
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "The Nature of Weather Persistence", [
        "Atmospheric Persistence: Weather conditions exhibit high autocorrelation; wet days tend to follow wet days due to ground moisture and low pressure.",
        "Deterministic Complexity: The Navier-Stokes equations governing atmospheric fluid flow are chaotic and computationally intractable for long-range planning.",
        "Probabilistic Need: Agriculture, logistics, and resource management require probability distributions of weather states rather than single deterministic point forecasts.",
        "The Markov Solution: Provides a rigorous mathematical framework modeling transition frequencies between observable weather states."
    ], border_color=OCEAN_BLUE)

    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Core Project Objectives", [
        "Construct a Discrete-Time Markov Chain (DTMC) modeling daily transitions between Sunny and Rainy states.",
        "Implement row-stochastic transition matrices using basic vector-matrix dot products.",
        "Numerically reproduce exact multi-step forecasting benchmarks (Day 1: [0.70, 0.30], Day 2: [0.61, 0.39]).",
        "Derive and prove the unique long-term stationary distribution (π = [4/7, 3/7] ≈ [57.14%, 42.86%]).",
        "Deploy a production-grade, interactive web application on Streamlit Community Cloud."
    ], border_color=AMBER)

    # ---------------- SLIDE 3: WHAT IS A MARKOV CHAIN? ----------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Theoretical Background: What is a Markov Chain?")
    add_card(s3, Inches(0.8), Inches(1.8), Inches(11.6), Inches(5.0), "Foundations of Discrete-Time Markov Chains (DTMC)", [
        "Definition: A sequence of random variables {X₀, X₁, X₂, ...} defined over a discrete state space S.",
        "Stochastic Process: Unlike deterministic systems, the state of the system at time t is governed by probability distributions.",
        "Time Homogeneity: Transition probabilities P(X_{t+1} = j | X_t = i) are stationary and independent of time t.",
        "State Space Topology: S = {S₁, S₂} where states are mutually exclusive and collectively exhaustive.",
        "The Fundamental Question: Given the present weather today, what is the probability distribution of weather n days into the future?"
    ])

    # ---------------- SLIDE 4: THE MARKOV PROPERTY (MEMORYLESSNESS) ----------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "The Markov Property: Mathematical Definition & Intuition")
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Formal Mathematical Axiom", [
        "Order-1 Markov Property Equation:",
        "P(X_{t+1} = s | X_t = x_t, X_{t-1} = x_{t-1}, ..., X_0 = x_0) = P(X_{t+1} = s | X_t = x_t)",
        "",
        "Conditional Independence: The conditional probability of the future state given both past and present states depends ONLY upon the present state.",
        "Information Sufficiency: Today's weather encapsulates all relevant predictive information; the past historical trajectory provides zero added predictive power in this model."
    ], border_color=OCEAN_BLUE)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Intuitive Weather Example", [
        "Scenario A: It was Sunny for 14 consecutive days, and today is Sunny.",
        "Scenario B: It rained heavily for 14 consecutive days, but cleared up today (Sunny).",
        "",
        "The Markov Prediction: In BOTH scenarios, the probability of Rain tomorrow is EXACTLY P(Rain | Sunny) = 0.30.",
        "Mathematical Advantage: Eliminates exponential historical complexity and reduces calculation to compact matrix multiplication."
    ], border_color=GREEN)

    # ---------------- SLIDE 5: STATE SPACE & TRANSITION PROBABILITIES ----------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "State Space Definition & Conditional Probabilities")
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "State Space S", [
        "Binary Discrete State Space: S = {Sunny, Rainy}",
        "S₁ = Sunny: Represents dry, clear, or partially cloudy weather without measurable precipitation.",
        "S₂ = Rainy: Represents weather with precipitation.",
        "",
        "Exhaustive Property: Any given day MUST be classified into exactly one of these two states.",
        "Mutually Exclusive: S₁ ∩ S₂ = ∅ (A day cannot be simultaneously classified as both states in the model)."
    ])

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "The Four Transition Probabilities", [
        "P(Sunny | Sunny) = 0.70: 70% probability a sunny day continues into another sunny day.",
        "P(Rainy | Sunny) = 0.30: 30% probability a sunny day transitions into rainfall.",
        "P(Sunny | Rainy) = 0.40: 40% probability a rainy day clears up into sunshine.",
        "P(Rainy | Rainy) = 0.60: 60% probability a rainy day persists into continued rainfall.",
        "",
        "Observation: Both states exhibit positive persistence (0.70 > 0.30 and 0.60 > 0.40)."
    ])

    # ---------------- SLIDE 6: THE TRANSITION MATRIX P ----------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "The Transition Probability Matrix (P) & Row Stochasticity")
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Matrix Formulation", [
        "Matrix Structure P:",
        "P = [[ P(Sunny|Sunny) , P(Rainy|Sunny) ],",
        "     [ P(Sunny|Rainy) , P(Rainy|Rainy) ]]",
        "",
        "Numerical Values:",
        "P = [[ 0.70 , 0.30 ],",
        "     [ 0.40 , 0.60 ]]",
        "",
        "Rows represent the CURRENT state (Given state today).",
        "Columns represent the DESTINATION state (Predicted state tomorrow)."
    ], border_color=OCEAN_BLUE)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Row-Stochastic Axiom Proof", [
        "Mathematical Rule: Every row of a Markov transition matrix must sum strictly to 1.0:",
        "Σ_{j} P_ij = 1  for all rows i",
        "",
        "Row 1 Check (Given Sunny today):",
        "P(Sunny|Sunny) + P(Rainy|Sunny) = 0.70 + 0.30 = 1.00 (100%)",
        "",
        "Row 2 Check (Given Rainy today):",
        "P(Sunny|Rainy) + P(Rainy|Rainy) = 0.40 + 0.60 = 1.00 (100%)",
        "",
        "Physical Meaning: Because the sample space is exhaustive, tomorrow's weather cannot fail to occur."
    ], border_color=AMBER)

    # ---------------- SLIDE 7: MULTI-STEP FORECASTING ----------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Multi-Step Forecasting: Chapman-Kolmogorov Theorem")
    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.6), Inches(5.0), "Forecasting Across Multiple Time Horizons", [
        "State Vector Notation: Let π_t = [P(X_t = Sunny), P(X_t = Rainy)] represent the probability distribution at Day t.",
        "1-Step Forward Equation: π_{t+1} = π_t × P",
        "2-Step Forward Equation: π_{t+2} = π_{t+1} × P = (π_t × P) × P = π_t × P²",
        "General n-Step Forecasting Equation: π_n = π_0 × Pⁿ",
        "",
        "Chapman-Kolmogorov Theorem: P_{ij}^{(m+n)} = Σ_k P_{ik}^{(m)} P_{kj}^{(n)}",
        "Significance: Matrix power Pⁿ represents the transition probabilities over an n-day interval without needing to track intermediate states."
    ])

    # ---------------- SLIDE 8: DAY 1 STEP-BY-STEP CALCULATION ----------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Numerical Execution: Day 1 Step-by-Step Dot Product")
    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Initial Conditions & Setup", [
        "Initial State Vector at Day 0: π₀ = [1.0, 0.0]",
        "Physical Interpretation: Today is 100% Sunny and 0% Rainy.",
        "",
        "Matrix Equation:",
        "π₁ = π₀ × P = [1.0, 0.0] × [[0.70, 0.30],",
        "                            [0.40, 0.60]]",
        "",
        "Vector-matrix dot product computes each destination state by weighting incoming probabilities."
    ])

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Explicit Dot Product Arithmetic", [
        "1. Calculating P(Sunny on Day 1):",
        "P(Sunny₁) = [π_{0,Sunny} × P_SS] + [π_{0,Rainy} × P_RS]",
        "          = [1.0 × 0.70] + [0.0 × 0.40]",
        "          = 0.7000 + 0.0000 = 0.7000 (70.0%)",
        "",
        "2. Calculating P(Rainy on Day 1):",
        "P(Rainy₁) = [π_{0,Sunny} × P_SR] + [π_{0,Rainy} × P_RR]",
        "          = [1.0 × 0.30] + [0.0 × 0.60]",
        "          = 0.3000 + 0.0000 = 0.3000 (30.0%)",
        "",
        "Day 1 Output: π₁ = [0.7000, 0.3000]  (Sum = 1.0000)"
    ], border_color=GREEN)

    # ---------------- SLIDE 9: DAY 2 STEP-BY-STEP CALCULATION ----------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Numerical Execution: Day 2 Step-by-Step Dot Product")
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Day 1 Distribution Input", [
        "State Vector from Day 1: π₁ = [0.70, 0.30]",
        "Physical Interpretation: 70% chance of Sunny, 30% chance of Rainy.",
        "",
        "Matrix Equation:",
        "π₂ = π₁ × P = [0.70, 0.30] × [[0.70, 0.30],",
        "                            [0.40, 0.60]]",
        "",
        "Both branches (Sunny and Rainy from Day 1) now contribute to Day 2 outcomes."
    ])

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Explicit Dot Product Arithmetic", [
        "1. Calculating P(Sunny on Day 2):",
        "P(Sunny₂) = [π_{1,Sunny} × P_SS] + [π_{1,Rainy} × P_RS]",
        "          = [0.70 × 0.70] + [0.30 × 0.40]",
        "          = 0.4900 + 0.1200 = 0.6100 (61.0%)",
        "",
        "2. Calculating P(Rainy on Day 2):",
        "P(Rainy₂) = [π_{1,Sunny} × P_SR] + [π_{1,Rainy} × P_RR]",
        "          = [0.70 × 0.30] + [0.30 × 0.60]",
        "          = 0.2100 + 0.1800 = 0.3900 (39.0%)",
        "",
        "Day 2 Output: π₂ = [0.6100, 0.3900]  (Sum = 1.0000)"
    ], border_color=GREEN)

    # ---------------- SLIDE 10: CONVERGENCE TRAJECTORY ----------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Trajectory Analysis: Multi-Day Convergence")
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Day-by-Day Forecast Trajectory", [
        "Day 0: π₀ = [1.0000, 0.0000] (100.0% Sunny,   0.0% Rainy)",
        "Day 1: π₁ = [0.7000, 0.3000] ( 70.0% Sunny,  30.0% Rainy)",
        "Day 2: π₂ = [0.6100, 0.3900] ( 61.0% Sunny,  39.0% Rainy)",
        "Day 3: π₃ = [0.5830, 0.4170] ( 58.3% Sunny,  41.7% Rainy)",
        "Day 4: π₄ = [0.5749, 0.4251] ( 57.5% Sunny,  42.5% Rainy)",
        "Day 5: π₅ = [0.5725, 0.4275] ( 57.2% Sunny,  42.8% Rainy)",
        "Day 6: π₆ = [0.5717, 0.4283] ( 57.1% Sunny,  42.9% Rainy)"
    ])

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Key Mathematical Observations", [
        "Rapid Damping: Day-to-day changes shrink exponentially with each step.",
        "Asymptotic Stability: The probabilities converge toward a constant limit.",
        "Independence of Initial State: Even if we start with π₀ = [0.0, 1.0] (100% Rainy), Day 5 converges to the exact same distribution!",
        "",
        "Theoretical Limit: lim_{n→∞} π_n = π (The Steady-State Equilibrium)."
    ], border_color=AMBER)

    # ---------------- SLIDE 11: STEADY STATE ALGEBRAIC DERIVATION ----------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Steady-State Distribution: Full Algebraic Derivation")
    add_card(s11, Inches(0.8), Inches(1.8), Inches(11.6), Inches(5.0), "Exact Step-by-Step Proof", [
        "Definition: Stationary distribution vector π = [π_S, π_R] satisfies π × P = π with π_S + π_R = 1.",
        "Matrix Equation: [π_S, π_R] × [[0.70, 0.30], [0.40, 0.60]] = [π_S, π_R]",
        "",
        "Step 1: Expand Column 1: π_S = 0.70 π_S + 0.40 π_R",
        "Step 2: Isolate variables: π_S - 0.70 π_S = 0.40 π_R  ===>  0.30 π_S = 0.40 π_R",
        "Step 3: Express π_S in terms of π_R: π_S = (0.40 / 0.30) π_R = (4/3) π_R",
        "Step 4: Substitute into Normalization constraint (π_S + π_R = 1):",
        "        (4/3) π_R + π_R = 1  ===>  (7/3) π_R = 1  ===>  π_R = 3/7 ≈ 0.428571 (42.86%)",
        "Step 5: Solve for π_S: π_S = 1 - (3/7) = 4/7 ≈ 0.571429 (57.14%)",
        "",
        "Final Invariant Vector: π = [4/7, 3/7] ≈ [0.5714, 0.4286]"
    ], border_color=GREEN)

    # ---------------- SLIDE 12: SPECTRAL ANALYSIS & EIGENVALUES ----------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Advanced Linear Algebra: Spectral Analysis & Eigenvalues")
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Eigenvalues of Matrix P", [
        "Characteristic Equation: det(P - λI) = 0",
        "det([[0.7 - λ, 0.3], [0.4, 0.6 - λ]]) = 0",
        "(0.7 - λ)(0.6 - λ) - (0.3)(0.4) = 0",
        "λ² - 1.3λ + 0.42 - 0.12 = 0",
        "λ² - 1.3λ + 0.30 = 0  ===>  (λ - 1.0)(λ - 0.3) = 0",
        "",
        "Eigenvalues: λ₁ = 1.0 ,  λ₂ = 0.30"
    ], border_color=OCEAN_BLUE)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Convergence Rate & Spectral Gap", [
        "Perron-Frobenius Theorem: Every stochastic matrix has a dominant eigenvalue λ₁ = 1.0.",
        "Stationary Eigenvector: The left eigenvector corresponding to λ₁ = 1 is the steady-state π.",
        "Rate of Convergence: Governed by the second eigenvalue λ₂ = 0.30.",
        "Error at Step n: ||π_n - π|| ≤ C × |λ₂|ⁿ = C × (0.3)ⁿ",
        "",
        "Exponential Damping: Because |λ₂| = 0.3 < 1, the deviation shrinks by 70% each day! This explains why convergence occurs within 5 days."
    ], border_color=AMBER)

    # ---------------- SLIDE 13: SOFTWARE ARCHITECTURE ----------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Software Architecture: Modular Python Design")
    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Separation of Concerns (MVC Pattern)", [
        "markov_model.py (Model):",
        "  • Pure NumPy matrix engine.",
        "  • Implements validate_transition_matrix, predict_next_day, predict_n_days.",
        "  • Analytical (4/7, 3/7) and linear algebra steady-state solvers.",
        "  • Step-by-step arithmetic generator.",
        "",
        "visualization.py (View - Graphics):",
        "  • Plotly interactive time-series trajectories.",
        "  • Interactive steady-state donut charts.",
        "  • Single-day probability comparison bar charts."
    ])

    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Dashboard & Quality Control", [
        "app.py (Controller & Dashboard):",
        "  • Streamlit interactive web interface.",
        "  • Dynamic sliders for day horizons and transition probabilities.",
        "  • Metric cards showing delta from Day 0.",
        "  • Pure LaTeX rendering using st.latex.",
        "",
        "test_markov_model.py (Automated Validation):",
        "  • Complete unit test assertions for Day 1, Day 2, and steady state.",
        "  • Invariance property check: π × P == π."
    ])

    # ---------------- SLIDE 14: INTERACTIVE APPLICATION DEMO ----------------
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Interactive Web Dashboard Features")
    add_card(s14, Inches(0.8), Inches(1.8), Inches(11.6), Inches(5.0), "User Interface & Educational Capabilities", [
        "1. Dynamic Weather Selection: Toggle between 100% Sunny, 100% Rainy, or custom initial distributions.",
        "2. Flexible Horizon Slider: Adjust forecasting from 1 day up to 20 days forward in real-time.",
        "3. Climate Simulation: Uncheck default matrix to test desert conditions (P_SS = 0.95) or tropical monsoon climates.",
        "4. Step-by-Step Calculator Tab: Select any day to see the exact numerical multiplication breakdown.",
        "5. Mathematical Theory Tab: Displays formal equations, matrix explanations, and proofs rendered cleanly in KaTeX.",
        "6. Scope & Limitations Tab: Clearly educates users on the boundary between stochastic models and real meteorology."
    ], bg_color=LIGHT_BG, border_color=OCEAN_BLUE)

    # ---------------- SLIDE 15: MODEL VALIDATION & TEST RESULTS ----------------
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Model Validation & Benchmark Verification")
    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Verification Benchmarks", [
        "Initial Distribution π₀ = [1.0, 0.0]",
        "",
        "✓ Benchmark 1: Day 1 Forecast",
        "  Target: [0.7000, 0.3000] | Result: PASS",
        "",
        "✓ Benchmark 2: Day 2 Forecast",
        "  Target: [0.6100, 0.3900] | Result: PASS",
        "",
        "✓ Benchmark 3: Long-Run Steady State",
        "  Target: [0.5714, 0.4286] (4/7, 3/7) | Result: PASS",
        "",
        "✓ Benchmark 4: Invariance Property",
        "  Target: π × P == π | Result: PASS"
    ], border_color=GREEN)

    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Automated Testing Output", [
        "Test Script: test_markov_model.py",
        "Assertions: 8 automated unit test assertions executed.",
        "",
        "Row Sum Axiom Check:",
        "  Row 0 Sum = 0.70 + 0.30 = 1.0000 ✓",
        "  Row 1 Sum = 0.40 + 0.60 = 1.0000 ✓",
        "",
        "Float Precision Tolerance: atol = 1e-5",
        "Result: 100% Test Pass with Zero Assertion Errors."
    ], border_color=OCEAN_BLUE)

    # ---------------- SLIDE 16: PHYSICAL METEOROLOGY VS STOCHASTIC MODELS ----------------
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Critical Limitations: Stochastic Models vs. Real Meteorology")
    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Simplified Markov Model", [
        "State Space: 2 discrete categories (Sunny, Rainy).",
        "Governing Dynamics: Fixed transition probability matrix P.",
        "Memory: 1-day memoryless property (Markovian).",
        "Spatial Dimension: Zero-dimensional (single localized point).",
        "Chaos & Divergence: None; converges smoothly to steady-state.",
        "Role: Climatological baseline, risk analysis, educational vehicle."
    ], border_color=AMBER)

    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0), "Real Numerical Weather Prediction (NWP)", [
        "State Space: Continuous 3D vector fields (temperature, pressure, humidity, wind vectors).",
        "Governing Dynamics: Navier-Stokes partial differential equations & thermodynamics.",
        "Memory: Multi-day atmospheric inertia (jet streams, frontal boundaries, oceanic currents).",
        "Spatial Dimension: Millions of 3D grid cells covering Earth.",
        "Chaos & Divergence: Highly non-linear (Lorenz attractor / Butterfly Effect).",
        "Role: Operational 1 to 10-day operational meteorological forecasting."
    ], border_color=DARK_BLUE)

    # ---------------- SLIDE 17: CONCLUSION & ACCESS LINKS ----------------
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Conclusion & Live Application Access")
    add_card(s17, Inches(0.8), Inches(1.8), Inches(11.6), Inches(5.0), "Summary & Live Access Links", [
        "1. Mathematical Success: Successfully formalized and verified a Discrete-Time Markov Chain for probabilistic weather modeling.",
        "2. Exact Reproduction: All calculations match presentation requirements (Day 1: [0.7, 0.3], Day 2: [0.61, 0.39], Steady State: [4/7, 3/7]).",
        "3. Educational Impact: Demonstrates matrix multiplication, spectral convergence, and probability axioms without black-box ML.",
        "4. Full Production Deployment: Live 24/7 on Streamlit Cloud and backed up on GitHub.",
        "",
        "🔗 Live Web Dashboard: https://5frtkkawtnf5aazokkb8ar.streamlit.app/",
        "🐙 GitHub Repository: https://github.com/sivakesavacodes/-weather-markov-predictor"
    ], bg_color=LIGHT_BG, border_color=GREEN)

    if os.path.exists(output_path):
        os.remove(output_path)
    prs.save(output_path)
    print(f"Expanded presentation (17 slides) saved to: {output_path}")


# -----------------------------------------------------------------------------
# 2. GENERATE EXPANDED WORD DOCUMENT REPORT
# -----------------------------------------------------------------------------
def build_word_document(output_path: str):
    doc = Document()

    for section in doc.sections:
        section.top_margin = DocxInches(1.0)
        section.bottom_margin = DocxInches(1.0)
        section.left_margin = DocxInches(1.0)
        section.right_margin = DocxInches(1.0)

    NAVY = DocxRGBColor(30, 58, 138)
    DARK = DocxRGBColor(31, 41, 55)

    def add_custom_heading(text, level):
        h = doc.add_heading(text, level=level)
        h.paragraph_format.space_before = DocxPt(14)
        h.paragraph_format.space_after = DocxPt(4)
        run = h.runs[0]
        run.font.color.rgb = NAVY
        return h

    # Title Header
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = DocxPt(4)
    run_t = p_title.add_run("MARKOV WEATHER PREDICTOR")
    run_t.font.size = DocxPt(26)
    run_t.font.bold = True
    run_t.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = DocxPt(16)
    run_sub = p_sub.add_run("A Stochastic Process Model for Weather Forecasting & Convergence Analysis using Discrete-Time Markov Chains")
    run_sub.font.size = DocxPt(13)
    run_sub.font.italic = True

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = DocxPt(20)
    r_meta = p_meta.add_run("Author: Siva Kesava | GitHub: sivakesavacodes\nLive Web Dashboard: https://5frtkkawtnf5aazokkb8ar.streamlit.app/")
    r_meta.font.size = DocxPt(10)
    r_meta.font.color.rgb = DocxRGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = DocxPt(10)

    # ABSTRACT
    add_custom_heading("ABSTRACT", level=1)
    p_abs = doc.add_paragraph(
        "Weather prediction is traditionally addressed through computationally intensive Numerical Weather Prediction (NWP) systems that discretize "
        "atmospheric fluid flow via the non-linear Navier-Stokes partial differential equations. However, for baseline risk modeling, agricultural planning, "
        "and stochastic process analysis, Discrete-Time Markov Chains (DTMC) offer an analytically rigorous and computationally elegant methodology. "
        "This project monograph details the design, mathematical formulation, numerical execution, spectral analysis, and cloud deployment of the "
        "'Markov Weather Predictor'. Modeling daily weather across a binary discrete state space S = {Sunny, Rainy} governed by a 2x2 row-stochastic "
        "transition probability matrix P, this project explores multi-step forecasting via Chapman-Kolmogorov equations, validates the memoryless Markov "
        "property, and demonstrates the exponential convergence of state probabilities toward a unique invariant stationary distribution π = [4/7, 3/7] ≈ [0.5714, 0.4286]. "
        "Every mathematical benchmark (Day 1: [0.70, 0.30], Day 2: [0.61, 0.39]) is verified through explicit dot-product hand calculations and confirmed with automated "
        "unit test suites. Furthermore, spectral gap analysis (λ₁ = 1.0, λ₂ = 0.30) is conducted to mathematically explain the rapid 5-day convergence rate. "
        "The project is implemented in Python without black-box machine learning libraries, published open-source on GitHub, and deployed 24/7 on Streamlit Community Cloud."
    )
    p_abs.paragraph_format.line_spacing = 1.15

    # 1. INTRODUCTION
    add_custom_heading("1. INTRODUCTION & PROBLEM MOTIVATION", level=1)
    doc.add_paragraph(
        "Weather systems exhibit a well-documented phenomenon known as meteorological persistence: today's atmospheric conditions strongly bias "
        "tomorrow's weather due to localized thermodynamic inertia, surface moisture, and synoptic pressure fields. A sunny day is statistically "
        "more likely to be followed by another sunny day than by an abrupt severe rainstorm.\n\n"
        "In probability theory and applied mathematics, systems that transition among discrete states over sequential time epochs according to probabilistic "
        "rules are known as stochastic processes. When transition probabilities depend exclusively on the current state rather than the extensive historical "
        "pathway, the system constitutes a Markov Chain, first formalized by Russian mathematician Andrey Markov in 1906.\n\n"
        "The objective of this project is threefold:\n"
        "1. To formulate and implement a two-state Discrete-Time Markov Chain (DTMC) modeling daily weather transitions.\n"
        "2. To mathematically derive, hand-calculate, and computationally verify multi-step forecasts and long-term equilibrium distributions.\n"
        "3. To build a modern, interactive web dashboard using Streamlit and Plotly that exposes intermediate calculations for educational transparency, "
        "and deploy it permanently online."
    )

    # 2. MATHEMATICAL FOUNDATION
    add_custom_heading("2. MATHEMATICAL FOUNDATIONS OF DISCRETE-TIME MARKOV CHAINS", level=1)
    
    add_custom_heading("2.1 State Space Definition", level=2)
    doc.add_paragraph(
        "Let {X_t : t ∈ {0, 1, 2, ...}} be a discrete-time stochastic process defined on a finite state space S:\n"
        "    S = { S₁: Sunny, S₂: Rainy }\n\n"
        "The state space satisfies two fundamental axioms:\n"
        "1. Mutually Exclusive: S₁ ∩ S₂ = ∅ (A single day cannot simultaneously be classified as both Sunny and Rainy).\n"
        "2. Collectively Exhaustive: S₁ ∪ S₂ = S (Every observed day must fall into one of the designated states)."
    )

    add_custom_heading("2.2 Conditional Transition Probabilities", level=2)
    doc.add_paragraph(
        "The transition probability P_ij represents the conditional probability of transitioning from state i at time t to state j at time t+1:\n"
        "    P_ij = P(X_{t+1} = j | X_t = i)\n\n"
        "From historical weather observations, the transition probabilities are specified as:\n"
        "    • P(Sunny | Sunny) = 0.70  (70% probability that Sunny continues into Sunny)\n"
        "    • P(Rainy | Sunny) = 0.30  (30% probability that Sunny turns into Rainy)\n"
        "    • P(Sunny | Rainy) = 0.40  (40% probability that Rainy clears into Sunny)\n"
        "    • P(Rainy | Rainy) = 0.60  (60% probability that Rainy continues into Rainy)"
    )

    add_custom_heading("2.3 Transition Probability Matrix P and Row Stochasticity", level=2)
    doc.add_paragraph(
        "These transition probabilities are organized into the 2x2 Transition Probability Matrix P:\n\n"
        "         |  Next Day Sunny (j=1)  |  Next Day Rainy (j=2)  |\n"
        "    P =  |------------------------|------------------------|\n"
        "    Sunny|          0.70          |          0.30          |\n"
        "    Rainy|          0.40          |          0.60          |\n\n"
        "A square matrix P is row-stochastic if and only if it satisfies:\n"
        "1. P_ij ≥ 0 for all i, j ∈ S\n"
        "2. Σ_{j∈S} P_ij = 1 for all rows i ∈ S\n\n"
        "Verification:\n"
        "    Row 1 (Sunny): 0.70 + 0.30 = 1.0000 (100%)\n"
        "    Row 2 (Rainy): 0.40 + 0.60 = 1.0000 (100%)\n\n"
        "Physical Justification: Because the states are exhaustive, a day that begins in state i must transition to some valid state in S tomorrow with probability 1."
    )

    add_custom_heading("2.4 The First-Order Markov Property (Memorylessness)", level=2)
    doc.add_paragraph(
        "The defining condition of the process is the first-order Markov property:\n\n"
        "    P(X_{t+1} = s | X_t = x_t, X_{t-1} = x_{t-1}, ..., X_0 = x_0) = P(X_{t+1} = s | X_t = x_t)\n\n"
        "This states that the conditional probability distribution of future states depends solely on the current state X_t, and is conditionally "
        "independent of the preceding trajectory X_{t-1}, ..., X_0.\n\n"
        "Example: If today is Sunny, the probability of rainfall tomorrow is exactly 0.30, regardless of whether it was preceded by a two-week drought "
        "or a multi-day monsoon. This assumption dramatically simplifies the joint probability calculation from an exponential tree into recursive matrix multiplication."
    )

    add_custom_heading("2.5 Multi-Step Forecasting & Chapman-Kolmogorov Theorem", level=2)
    doc.add_paragraph(
        "Let π_t = [P(X_t = Sunny), P(X_t = Rainy)] be a 1x2 row vector denoting the probability distribution at time t.\n"
        "The 1-step forecast is given by vector-matrix multiplication:\n"
        "    π_{t+1} = π_t * P\n\n"
        "By mathematical induction, forecasting n days into the future from initial distribution π_0 yields:\n"
        "    π_n = π_0 * Pⁿ\n\n"
        "According to the Chapman-Kolmogorov theorem, the n-step transition matrix Pⁿ satisfies:\n"
        "    P_{ij}^{(m+n)} = Σ_{k∈S} P_{ik}^{(m)} P_{kj}^{(n)}\n"
        "This guarantees that intermediate paths are integrated consistently across all possible states."
    )

    # 3. NUMERICAL BENCHMARKS
    add_custom_heading("3. NUMERICAL STEP-BY-STEP HAND CALCULATIONS", level=1)
    doc.add_paragraph(
        "To satisfy rigorous verification criteria, we establish initial conditions where Day 0 is 100% Sunny:\n"
        "    π_0 = [1.0, 0.0]\n\n"
        "We now compute Day 1 and Day 2 forecasts explicitly using vector-matrix dot products."
    )

    add_custom_heading("3.1 Day 1 Forecast (π₁ = π₀ * P)", level=2)
    doc.add_paragraph(
        "Matrix Dot Product:\n"
        "    π₁ = [1.0, 0.0] * [[0.70, 0.30],\n"
        "                       [0.40, 0.60]]\n\n"
        "Calculating P(Sunny on Day 1):\n"
        "    P(Sunny₁) = [π_{0,Sunny} * P_SS] + [π_{0,Rainy} * P_RS]\n"
        "              = [1.0 * 0.70] + [0.0 * 0.40] = 0.7000 (70.0%)\n\n"
        "Calculating P(Rainy on Day 1):\n"
        "    P(Rainy₁) = [π_{0,Sunny} * P_SR] + [π_{0,Rainy} * P_RR]\n"
        "              = [1.0 * 0.30] + [0.0 * 0.60] = 0.3000 (30.0%)\n\n"
        "Result: π₁ = [0.7000, 0.3000]  |  Sum = 0.7000 + 0.3000 = 1.0000"
    )

    add_custom_heading("3.2 Day 2 Forecast (π₂ = π₁ * P)", level=2)
    doc.add_paragraph(
        "Matrix Dot Product:\n"
        "    π₂ = [0.70, 0.30] * [[0.70, 0.30],\n"
        "                         [0.40, 0.60]]\n\n"
        "Calculating P(Sunny on Day 2):\n"
        "    P(Sunny₂) = [π_{1,Sunny} * P_SS] + [π_{1,Rainy} * P_RS]\n"
        "              = [0.70 * 0.70] + [0.30 * 0.40]\n"
        "              = 0.4900 + 0.1200 = 0.6100 (61.0%)\n\n"
        "Calculating P(Rainy on Day 2):\n"
        "    P(Rainy₂) = [π_{1,Sunny} * P_SR] + [π_{1,Rainy} * P_RR]\n"
        "              = [0.70 * 0.30] + [0.30 * 0.60]\n"
        "              = 0.2100 + 0.1800 = 0.3900 (39.0%)\n\n"
        "Result: π₂ = [0.6100, 0.3900]  |  Sum = 0.6100 + 0.3900 = 1.0000"
    )

    # Verification Table
    add_custom_heading("3.3 Trajectory Summary Table", level=2)
    table = doc.add_table(rows=8, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Day (n)", "Mathematical Form", "P(Sunny)", "P(Rainy)", "Row Sum Axiom"]
    for idx, h in enumerate(headers):
        cell = table.cell(0, idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = NAVY

    benchmarks = [
        ["Day 0", "π_0", "1.0000 (100.0%)", "0.0000 (0.0%)", "1.0000"],
        ["Day 1", "π_0 * P", "0.7000 (70.0%)", "0.3000 (30.0%)", "1.0000"],
        ["Day 2", "π_1 * P", "0.6100 (61.0%)", "0.3900 (39.0%)", "1.0000"],
        ["Day 3", "π_2 * P", "0.5830 (58.3%)", "0.4170 (41.7%)", "1.0000"],
        ["Day 4", "π_3 * P", "0.5749 (57.5%)", "0.4251 (42.5%)", "1.0000"],
        ["Day 5", "π_4 * P", "0.5725 (57.2%)", "0.4275 (42.8%)", "1.0000"],
        ["Steady State", "lim_{n->inf} π_n", "0.5714 (57.14%)", "0.4286 (42.86%)", "1.0000"]
    ]

    for r_idx, r_data in enumerate(benchmarks, start=1):
        for c_idx, val in enumerate(r_data):
            table.cell(r_idx, c_idx).text = val

    doc.add_paragraph().paragraph_format.space_after = DocxPt(12)

    # 4. STEADY STATE DERIVATION & SPECTRAL ANALYSIS
    add_custom_heading("4. STATIONARY DISTRIBUTION & SPECTRAL EIGENVALUE ANALYSIS", level=1)
    
    add_custom_heading("4.1 Complete Algebraic Derivation of π", level=2)
    doc.add_paragraph(
        "A distribution vector π = [π_S, π_R] is a stationary (steady-state) distribution of the chain if:\n"
        "    π * P = π   subject to   π_S + π_R = 1\n\n"
        "Expanding into simultaneous equations:\n"
        "    [π_S, π_R] * [[0.70, 0.30],\n"
        "                 [0.40, 0.60]] = [π_S, π_R]\n\n"
        "Equating column 1:\n"
        "    0.70 π_S + 0.40 π_R = π_S\n"
        "    0.40 π_R = π_S - 0.70 π_S\n"
        "    0.40 π_R = 0.30 π_S  ===>  π_S = (0.40 / 0.30) π_R = (4/3) π_R\n\n"
        "Equating column 2:\n"
        "    0.30 π_S + 0.60 π_R = π_R\n"
        "    0.30 π_S = 0.40 π_R  (Identical relation, showing linear dependence)\n\n"
        "Substituting π_S = (4/3) π_R into the probability normalization constraint π_S + π_R = 1:\n"
        "    (4/3) π_R + π_R = 1\n"
        "    (7/3) π_R = 1  ===>  π_R = 3/7 ≈ 0.428571 (42.86%)\n"
        "    π_S = 1 - (3/7) = 4/7 ≈ 0.571429 (57.14%)\n\n"
        "Conclusion: In the long run, the system will spend 57.14% of days in the Sunny state and 42.86% in the Rainy state, regardless of initial conditions."
    )

    add_custom_heading("4.2 Advanced Spectral Analysis: Eigenvalues & Convergence Rate", level=2)
    doc.add_paragraph(
        "The stationary condition π * P = π is equivalent to finding the left eigenvector corresponding to eigenvalue λ = 1:\n"
        "    P^T * π^T = 1.0 * π^T\n\n"
        "We solve the characteristic polynomial det(P - λI) = 0:\n"
        "    det([[0.70 - λ, 0.30],\n"
        "         [0.40, 0.60 - λ]]) = (0.70 - λ)(0.60 - λ) - (0.30)(0.40) = 0\n"
        "    λ² - 1.30λ + 0.42 - 0.12 = 0\n"
        "    λ² - 1.30λ + 0.30 = 0\n"
        "    (λ - 1.0)(λ - 0.30) = 0\n\n"
        "The two eigenvalues are:\n"
        "    λ₁ = 1.00 (Dominant eigenvalue guaranteed by Perron-Frobenius theorem)\n"
        "    λ₂ = 0.30 (Subdominant eigenvalue)\n\n"
        "Rate of Convergence (Spectral Gap):\n"
        "The rate at which π_n converges to the steady-state π is governed by the second eigenvalue λ₂:\n"
        "    ||π_n - π|| ≤ C * |λ₂|ⁿ = C * (0.30)ⁿ\n\n"
        "Because |λ₂| = 0.30 < 1, the distance between the forecast and the equilibrium shrinks by 70% at every single step! "
        "At Day 5, (0.30)⁵ = 0.00243, explaining why convergence to 3 decimal places occurs in under 5 days."
    )

    # 5. SOFTWARE ARCHITECTURE
    add_custom_heading("5. SOFTWARE ENGINEERING & DEPLOYMENT ARCHITECTURE", level=1)
    doc.add_paragraph(
        "The codebase is constructed with a strict Model-View-Controller (MVC) architectural separation:\n\n"
        "• markov_model.py (Model): Implements pure NumPy matrix operations. Contains validate_transition_matrix (row-stochastic verification), "
        "predict_next_day (vector dot-products), predict_n_days (multi-step loops), and compute_steady_state_analytical.\n\n"
        "• visualization.py (View - Visuals): Houses interactive Plotly line charts, steady-state donut charts, and Matplotlib figure routines.\n\n"
        "• app.py (Controller - UI): A modern reactive Streamlit dashboard providing parameter sliders, interactive weather state toggles, "
        "step-by-step arithmetic inspection, and LaTeX formula displays.\n\n"
        "• test_markov_model.py (Quality Assurance): Automated unit test suite with 8 assertions verifying matrix properties, row sums, "
        "Day 1/Day 2 values, and steady-state invariance.\n\n"
        "• Cloud Infrastructure: Version-controlled on GitHub (github.com/sivakesavacodes/-weather-markov-predictor) and deployed permanently on "
        "Streamlit Community Cloud (https://5frtkkawtnf5aazokkb8ar.streamlit.app/)."
    )

    # 6. LIMITATIONS & NWP
    add_custom_heading("6. ACADEMIC LIMITATIONS: STOCHASTIC MODELS VS. REAL METEOROLOGY", level=1)
    doc.add_paragraph(
        "A rigorous academic defense must articulate the boundary between stochastic modeling and physical atmospheric science:\n\n"
        "1. Dimensionality: The Markov model operates on 2 discrete categories (Sunny, Rainy). Real meteorology measures continuous 3D vector fields "
        "(barometric pressure, temperature, relative humidity, wind velocity, vorticity).\n\n"
        "2. Physics vs. Probability: Physical forecasting uses Numerical Weather Prediction (NWP), integrating the Navier-Stokes equations for "
        "fluid flow, mass conservation, and thermodynamics. In contrast, Markov models estimate empirical state transition frequencies.\n\n"
        "3. Memory vs. Chaos: The Markov assumption presumes memorylessness. Real weather possesses significant atmospheric inertia (jet streams, monsoons) "
        "coupled with chaotic non-linear sensitivity to initial conditions (Lorenz attractor / Butterfly Effect).\n\n"
        "4. Application Value: While unsuitable for operational 24-hour storm tracking, Markov chains excel at long-term climatological risk modeling, "
        "seasonal reservoir inflow estimation, and serving as baseline benchmarks for machine learning models."
    )

    # 7. VIVA DEFENSE PREPARATION
    add_custom_heading("7. VIVA & ORAL EXAMINATION DEFENSE QUESTIONS", level=1)
    doc.add_paragraph(
        "Below are model answers for likely questions posed by academic examiners:\n\n"
        "Q1: Why must the rows of matrix P sum to 1.0, but not the columns?\n"
        "Answer: Each row represents the conditional probability distribution over all mutually exclusive destination states given a specific current state. "
        "By the total probability axiom, the system must transition to some valid state in S tomorrow with probability 1.0. Columns represent incoming probabilities "
        "from different source states and have no requirement to sum to 1.\n\n"
        "Q2: What happens if we start with Day 0 as 100% Rainy instead of Sunny?\n"
        "Answer: On Day 1, π₁ = [0.40, 0.60]. On Day 2, π₂ = [0.52, 0.48]. By Day 5, the distribution converges to the exact same steady state π = [4/7, 3/7] ≈ [0.5714, 0.4286]. "
        "The stationary distribution of an ergodic Markov chain is unique and independent of initial conditions.\n\n"
        "Q3: How does spectral gap explain the rate of convergence?\n"
        "Answer: The transition matrix has eigenvalues λ₁ = 1 and λ₂ = 0.30. The rate of decay toward steady state is bounded by |λ₂|ⁿ = (0.30)ⁿ. "
        "Because |λ₂| < 1, the error decays exponentially, explaining why the system stabilizes within 5 days."
    )

    # 8. CONCLUSION
    add_custom_heading("8. CONCLUSION & PROJECT LINKS", level=1)
    doc.add_paragraph(
        "The 'Markov Weather Predictor' successfully models weather transitions using Discrete-Time Markov Chains, providing transparent arithmetic, "
        "analytical proofs, and modern interactive cloud deployment.\n\n"
        "• Live Streamlit Web App: https://5frtkkawtnf5aazokkb8ar.streamlit.app/\n"
        "• GitHub Source Code: https://github.com/sivakesavacodes/-weather-markov-predictor"
    )

    if os.path.exists(output_path):
        os.remove(output_path)
    doc.save(output_path)
    print(f"Expanded report saved to: {output_path}")


if __name__ == "__main__":
    ppt_out = os.path.join(r"C:\Users\Siva\weather-markov-predictor", "MARKOV_WEATHER_PREDICTOR_PRESENTATION.pptx")
    doc_out = os.path.join(r"C:\Users\Siva\weather-markov-predictor", "MARKOV_WEATHER_PREDICTOR_REPORT.docx")
    
    build_powerpoint(ppt_out)
    build_word_document(doc_out)
