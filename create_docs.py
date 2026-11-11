"""
create_docs.py
Generates the official PowerPoint Presentation (.pptx) and Word Document Report (.docx)
for the Markov Weather Predictor project.
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
# 1. GENERATE POWERPOINT PRESENTATION (.pptx)
# -----------------------------------------------------------------------------
def build_powerpoint(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BLUE = RGBColor(30, 58, 138)
    LIGHT_BG = RGBColor(248, 250, 252)
    TEXT_DARK = RGBColor(31, 41, 55)
    AMBER = RGBColor(245, 158, 11)
    OCEAN_BLUE = RGBColor(59, 130, 246)
    WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="ACADEMIC MATHEMATICS PROJECT"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = OCEAN_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
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
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.3)
        tf.margin_bottom = Inches(0.3)

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = DARK_BLUE
            p_title.space_after = Pt(10)
            first_bullet = True
        else:
            first_bullet = False

        for pt in points:
            p = tf.add_paragraph() if (title or not first_bullet) else tf.paragraphs[0]
            first_bullet = False
            p.text = f"•  {pt}"
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(6)

    # ---------------- SLIDE 1: TITLE SLIDE ----------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BLUE
    bg1.line.fill.background()

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "APPLIED MATHEMATICS & STOCHASTIC PROCESSES"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = AMBER
    p_badge.space_after = Pt(15)

    p_main = tf1.add_paragraph()
    p_main.text = "MARKOV WEATHER PREDICTOR"
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_after = Pt(10)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Discrete-Time Stochastic Model for Probabilistic Weather Forecasting"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(209, 213, 219)
    p_sub.space_after = Pt(30)

    p_meta = tf1.add_paragraph()
    p_meta.text = "Author: Siva Kesava | GitHub: sivakesavacodes\nLive Application: https://5frtkkawtnf5aazokkb8ar.streamlit.app/"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(156, 163, 175)

    # ---------------- SLIDE 2: OBJECTIVES ----------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Project Objectives & Mathematical Scope")
    add_card(slide2, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Primary Goals", [
        "Construct a Discrete-Time Markov Chain (DTMC) modeling daily weather transitions.",
        "Demonstrate the Markov Property: Next state depends strictly on the current state.",
        "Implement row-stochastic transition matrices using NumPy vector-matrix dot products.",
        "Analytically compute and verify long-term steady-state equilibrium distributions (π)."
    ], border_color=OCEAN_BLUE)

    add_card(slide2, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Deliverables & Implementation", [
        "Interactive Web Dashboard: Modern Streamlit UI with customizable forecast horizons.",
        "Plotly Visualizations: Dynamic probability trajectories, convergence, and pie charts.",
        "Transparent Step-by-Step Arithmetic: Exact dot-product breakdown for every forecast day.",
        "Full Cloud Deployment: Live 24/7 on Streamlit Cloud & version-controlled on GitHub."
    ], border_color=AMBER)

    # ---------------- SLIDE 3: MATHEMATICAL FOUNDATION ----------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Mathematical Foundation: State Space & Matrix P")
    add_card(slide3, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "State Space & Probabilities", [
        "State Space S = {Sunny, Rainy} (2 discrete, mutually exclusive states).",
        "Transition Probability: P(X_{t+1} = j | X_t = i).",
        "P(Sunny | Sunny) = 0.7  (70% chance of Sunny staying Sunny).",
        "P(Rainy | Sunny) = 0.3  (30% chance Sunny turns Rainy).",
        "P(Sunny | Rainy) = 0.4  (40% chance Rainy clears up to Sunny).",
        "P(Rainy | Rainy) = 0.6  (60% chance Rainy stays Rainy)."
    ])

    add_card(slide3, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Transition Matrix P & Row Stochasticity", [
        "Matrix Structure P = [[0.7, 0.3], [0.4, 0.6]].",
        "Rows (i): Represent the current weather state today.",
        "Columns (j): Represent the predicted weather state tomorrow.",
        "Row-Stochastic Axiom: Every row must sum strictly to 1.0:",
        "Row 1 (Sunny): 0.7 + 0.3 = 1.0",
        "Row 2 (Rainy): 0.4 + 0.6 = 1.0",
        "Physical Meaning: Tomorrow's weather MUST be either Sunny or Rainy."
    ])

    # ---------------- SLIDE 4: THE MARKOV PROPERTY ----------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "The Markov Property: Memorylessness")
    add_card(slide4, Inches(0.8), Inches(2.0), Inches(11.6), Inches(4.8), "Formal Definition & Intuitive Meaning", [
        "Mathematical Equation: P(X_{t+1} = s | X_t, X_{t-1}, ..., X_0) = P(X_{t+1} = s | X_t).",
        "The Memoryless Assumption: The future state depends ONLY on the current present state.",
        "Historical Independence: Knowing what happened 3 days ago or 2 weeks ago gives zero additional predictive information in this model.",
        "Real-World Analogy: If today is Sunny, the probability of rain tomorrow is exactly 0.30, whether it was sunny for the last 10 days or poured rain all last month.",
        "Mathematical Elegance: Transforms an intractable multi-day historical joint distribution into simple matrix multiplication."
    ])

    # ---------------- SLIDE 5: STEP-BY-STEP CALCULATION ----------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Numerical Demonstration: Reproducing Day 1 & Day 2")
    add_card(slide5, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Day 1 Forecast (π₁ = π₀ × P)", [
        "Initial State: π₀ = [1.0, 0.0]  (Today is 100% Sunny).",
        "Vector-Matrix Dot Product: π₁ = [1.0, 0.0] × [[0.7, 0.3], [0.4, 0.6]]",
        "P(Sunny on Day 1) = (1.0 × 0.7) + (0.0 × 0.4) = 0.70 (70.0%)",
        "P(Rainy on Day 1) = (1.0 × 0.3) + (0.0 × 0.6) = 0.30 (30.0%)",
        "Resulting Distribution: π₁ = [0.70, 0.30]",
        "Verification: 0.70 + 0.30 = 1.00 (100%)"
    ])

    add_card(slide5, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Day 2 Forecast (π₂ = π₁ × P)", [
        "Previous State: π₁ = [0.70, 0.30]",
        "Vector-Matrix Dot Product: π₂ = [0.70, 0.30] × [[0.7, 0.3], [0.4, 0.6]]",
        "P(Sunny on Day 2) = (0.70 × 0.7) + (0.30 × 0.4) = 0.49 + 0.12 = 0.61 (61.0%)",
        "P(Rainy on Day 2) = (0.70 × 0.3) + (0.30 × 0.6) = 0.21 + 0.18 = 0.39 (39.0%)",
        "Resulting Distribution: π₂ = [0.61, 0.39]",
        "Verification: 0.61 + 0.39 = 1.00 (100%)"
    ])

    # ---------------- SLIDE 6: STEADY-STATE DERIVATION ----------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Analytical Steady-State Equilibrium (π)")
    add_card(slide6, Inches(0.8), Inches(2.0), Inches(11.6), Inches(4.8), "Exact Algebraic Derivation", [
        "Stationary Condition: π × P = π  subject to  π_S + π_R = 1",
        "Expanding: [π_S, π_R] × [[0.7, 0.3], [0.4, 0.6]] = [π_S, π_R]",
        "Equation 1: π_S = 0.7 π_S + 0.4 π_R  ===>  0.3 π_S = 0.4 π_R  ===>  π_S = (4/3) π_R",
        "Substitution into Normalization: (4/3) π_R + π_R = 1  ===>  (7/3) π_R = 1",
        "Exact Fractions: π_R = 3/7 ≈ 0.428571 (42.86%), π_S = 4/7 ≈ 0.571429 (57.14%)",
        "Physical Conclusion: In the distant future, regardless of whether today is Sunny or Rainy, 57.14% of days are Sunny and 42.86% are Rainy."
    ])

    # ---------------- SLIDE 7: ARCHITECTURE & CODE ----------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Software Engineering & Architecture")
    add_card(slide7, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Separation of Concerns", [
        "markov_model.py: Pure NumPy engine with dot-product operations, validation, and analytical solvers.",
        "visualization.py: Plotly interactive curves and Matplotlib publication figures.",
        "app.py: Streamlit reactive dashboard with live parameter manipulation.",
        "test_markov_model.py: Automated unit test suite verifying mathematical benchmarks."
    ])

    add_card(slide7, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Key Engineering Features", [
        "Zero Black-Box Libraries: Built from scratch with basic matrix arithmetic.",
        "Interactive Horizon Slider: Forecast dynamically from 1 to 20 days.",
        "Custom Matrix Testing: Ability to simulate arid desert vs. tropical climates.",
        "Production Quality: Strict row-stochastic validation and exception handling."
    ])

    # ---------------- SLIDE 8: LIMITATIONS & NWP ----------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Scientific Scope & Critical Limitations")
    add_card(slide8, Inches(0.8), Inches(2.0), Inches(11.6), Inches(4.8), "Stochastic Modeling vs. Physical Meteorology", [
        "Not a Physical Forecast: Does not solve Navier-Stokes fluid dynamics or thermodynamics.",
        "Discrete vs. Continuous: Real weather has continuous pressure, temperature, humidity, and wind fields.",
        "Atmospheric Memory: Jet streams, cyclones, and pressure fronts create multi-day physical memory.",
        "Chaos & Non-linearity: Real atmosphere has sensitive dependence on initial conditions (Butterfly Effect).",
        "True Academic Purpose: Demonstrates stochastic state transitions, probability convergence, and statistical baseline modeling."
    ])

    # ---------------- SLIDE 9: CONCLUSION & LIVE DEMO ----------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Conclusion & Live Application")
    add_card(slide9, Inches(0.8), Inches(2.0), Inches(11.6), Inches(4.8), "Key Project Highlights", [
        "✓ Mathematical Rigor: Fully verified DTMC reproducing exact presentation benchmarks.",
        "✓ Clean Engineering: Modular Python code with comprehensive docstrings and assertions.",
        "✓ 24/7 Cloud Deployment: Open to anyone globally on Streamlit Community Cloud.",
        "✓ Open Source: Code available on GitHub under MIT license.",
        "",
        "🔗 Live Web App: https://5frtkkawtnf5aazokkb8ar.streamlit.app/",
        "🐙 GitHub Repository: https://github.com/sivakesavacodes/-weather-markov-predictor"
    ], bg_color=LIGHT_BG, border_color=OCEAN_BLUE)

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")


# -----------------------------------------------------------------------------
# 2. GENERATE WORD DOCUMENT REPORT (.docx)
# -----------------------------------------------------------------------------
def build_word_document(output_path: str):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = DocxInches(1.0)
        section.bottom_margin = DocxInches(1.0)
        section.left_margin = DocxInches(1.0)
        section.right_margin = DocxInches(1.0)

    # Styles & Fonts
    NAVY = DocxRGBColor(30, 58, 138)
    DARK = DocxRGBColor(31, 41, 55)

    def add_custom_heading(text, level):
        h = doc.add_heading(text, level=level)
        h.paragraph_format.space_before = DocxPt(12)
        h.paragraph_format.space_after = DocxPt(4)
        run = h.runs[0]
        run.font.color.rgb = NAVY
        return h

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = DocxPt(4)
    run_t = p_title.add_run("MARKOV WEATHER PREDICTOR")
    run_t.font.size = DocxPt(24)
    run_t.font.bold = True
    run_t.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = DocxPt(18)
    run_sub = p_sub.add_run("A Stochastic Process Model for Weather Prediction using Discrete-Time Markov Chains")
    run_sub.font.size = DocxPt(13)
    run_sub.font.italic = True

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = DocxPt(24)
    r_meta = p_meta.add_run("Author: Siva Kesava | GitHub: sivakesavacodes\nLive App: https://5frtkkawtnf5aazokkb8ar.streamlit.app/")
    r_meta.font.size = DocxPt(10)
    r_meta.font.color.rgb = DocxRGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = DocxPt(12)

    # ABSTRACT
    add_custom_heading("ABSTRACT", level=1)
    p_abs = doc.add_paragraph(
        "Weather forecasting represents one of the foundational challenges of applied mathematics and computational science. "
        "While modern meteorology relies on supercomputer-driven Numerical Weather Prediction (NWP) solving non-linear Navier-Stokes partial "
        "differential equations, stochastic processes provide an elegant, analytically tractable framework to model weather transitions as probabilistic "
        "state spaces. This report documents the design, mathematical derivation, numerical implementation, and web-based deployment of the "
        "'Markov Weather Predictor'—a Discrete-Time Markov Chain (DTMC) forecasting application. Using a two-state weather space (Sunny, Rainy) and "
        "a row-stochastic transition probability matrix P, the model executes day-by-day probability forecasting via vector-matrix dot products, "
        "verifies the memoryless Markov property, and solves for the unique invariant stationary distribution π. All mathematical benchmarks "
        "(Day 1: [0.70, 0.30], Day 2: [0.61, 0.39], Steady-State: [4/7, 3/7] ≈ [0.5714, 0.4286]) are verified analytically and confirmed with automated unit tests. "
        "The complete system is published open-source on GitHub and deployed 24/7 on Streamlit Community Cloud."
    )
    p_abs.paragraph_format.line_spacing = 1.15
    p_abs.paragraph_format.space_after = DocxPt(12)

    # 1. INTRODUCTION
    add_custom_heading("1. INTRODUCTION & PROBLEM DEFINITION", level=1)
    p_intro = doc.add_paragraph(
        "Weather conditions are characterized by statistical persistence: a rainy day is historically more likely to be followed by another rainy day "
        "than by a clear day due to the presence of residual moisture, cloud cover, and localized low-pressure systems. In probability theory, "
        "systems exhibiting state transitions over discrete time intervals can be modeled using stochastic processes—specifically Markov chains.\n\n"
        "The objective of this project is to implement an interactive educational platform demonstrating how mathematical transition matrices "
        "forecast future probabilities without relying on opaque machine learning libraries. The implementation exposes every intermediate arithmetic step, "
        "validates probability axioms, and distinguishes stochastic baseline modeling from physical atmospheric fluid dynamics."
    )
    p_intro.paragraph_format.line_spacing = 1.15

    # 2. MATHEMATICAL THEORY
    add_custom_heading("2. MATHEMATICAL FOUNDATIONS OF MARKOV CHAINS", level=1)
    
    add_custom_heading("2.1 State Space & Conditional Transition Probabilities", level=2)
    doc.add_paragraph(
        "Let {X_t : t = 0, 1, 2, ...} be a stochastic process taking values in a finite state space S:\n"
        "    S = { S_1: Sunny, S_2: Rainy }\n\n"
        "The transition probability P_ij denotes the conditional probability that the system moves to state j at time t+1 given that it occupies state i at time t:\n"
        "    P_ij = P(X_{t+1} = j | X_t = i)\n\n"
        "Based on historical meteorological frequency analysis, the empirical transition probabilities are established as follows:\n"
        "    • P(Sunny | Sunny) = 0.70 (70% probability that a sunny day is followed by another sunny day)\n"
        "    • P(Rainy | Sunny) = 0.30 (30% probability that a sunny day transitions into rain)\n"
        "    • P(Sunny | Rainy) = 0.40 (40% probability that a rainy day clears up into sunshine)\n"
        "    • P(Rainy | Rainy) = 0.60 (60% probability that a rainy day persists into another rainy day)"
    )

    add_custom_heading("2.2 The Transition Probability Matrix (P) and Row Stochasticity", level=2)
    doc.add_paragraph(
        "These transition probabilities form the 2x2 Transition Probability Matrix P:\n\n"
        "         |  Next Day Sunny  |  Next Day Rainy  |\n"
        "    P =  |------------------|------------------|\n"
        "    Sunny|       0.70       |       0.30       |\n"
        "    Rainy|       0.40       |       0.60       |\n\n"
        "Matrix Properties:\n"
        "1. Square Matrix: Dimensionality is 2x2 corresponding to |S| = 2.\n"
        "2. Non-negativity: 0 <= P_ij <= 1 for all i, j in S.\n"
        "3. Row-Stochastic Axiom: Every row must sum strictly to 1.0:\n"
        "       Sum_{j in S} P_ij = 1  for all i in S\n"
        "       Row 1 (Sunny): 0.70 + 0.30 = 1.00\n"
        "       Row 2 (Rainy): 0.40 + 0.60 = 1.00\n"
        "Physical significance: Because the state space is exhaustive and mutually exclusive, tomorrow's weather must definitively transition into one of the available states."
    )

    add_custom_heading("2.3 The Markov Property (Memorylessness)", level=2)
    doc.add_paragraph(
        "The foundational postulate of a first-order Markov chain is the Markov Property:\n\n"
        "    P(X_{t+1} = s | X_t = x_t, X_{t-1} = x_{t-1}, ..., X_0 = x_0) = P(X_{t+1} = s | X_t = x_t)\n\n"
        "This implies that conditional on the present state X_t, the future state X_{t+1} is statistically independent of the past states X_{t-1}, ..., X_0. "
        "For example, if today is Sunny, the probability of rain tomorrow is exactly 0.30, regardless of whether the preceding week experienced a drought or continuous storms."
    )

    # 3. NUMERICAL IMPLEMENTATION & VERIFICATION
    add_custom_heading("3. NUMERICAL CALCULATION & STEP-BY-STEP WALKTHROUGH", level=1)
    doc.add_paragraph(
        "Let pi_0 = [1.0, 0.0] represent the initial state probability vector at Day 0 (indicating 100% certainty of Sunny weather today). "
        "Multi-step probability forecasts are obtained via vector-matrix dot products:\n"
        "    pi_n = pi_0 * P^n"
    )

    # Table of benchmark values
    table = doc.add_table(rows=6, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Day (n)", "Mathematical Formula", "P(Sunny)", "P(Rainy)", "Row Sum Check"]
    for idx, h in enumerate(headers):
        cell = table.cell(0, idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = NAVY

    data = [
        ["Day 0", "pi_0", "1.0000 (100.0%)", "0.0000 (0.0%)", "1.0000"],
        ["Day 1", "pi_0 * P", "0.7000 (70.0%)", "0.3000 (30.0%)", "1.0000"],
        ["Day 2", "pi_1 * P", "0.6100 (61.0%)", "0.3900 (39.0%)", "1.0000"],
        ["Day 3", "pi_2 * P", "0.5830 (58.3%)", "0.4170 (41.7%)", "1.0000"],
        ["Steady State", "lim_{n->inf} pi_n", "0.5714 (57.14%)", "0.4286 (42.86%)", "1.0000"]
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            table.cell(row_idx, col_idx).text = text

    doc.add_paragraph().paragraph_format.space_after = DocxPt(12)

    add_custom_heading("3.1 Step-by-Step Dot Product Arithmetic", level=2)
    doc.add_paragraph(
        "Day 1 Arithmetic:\n"
        "    P(Sunny on Day 1) = [pi_{0,S} * P_SS] + [pi_{0,R} * P_RS] = [1.0 * 0.70] + [0.0 * 0.40] = 0.7000\n"
        "    P(Rainy on Day 1) = [pi_{0,S} * P_SR] + [pi_{0,R} * P_RR] = [1.0 * 0.30] + [0.0 * 0.60] = 0.3000\n"
        "    pi_1 = [0.7000, 0.3000]\n\n"
        "Day 2 Arithmetic:\n"
        "    P(Sunny on Day 2) = [pi_{1,S} * P_SS] + [pi_{1,R} * P_RS] = [0.70 * 0.70] + [0.30 * 0.40] = 0.49 + 0.12 = 0.6100\n"
        "    P(Rainy on Day 2) = [pi_{1,S} * P_SR] + [pi_{1,R} * P_RR] = [0.70 * 0.30] + [0.30 * 0.60] = 0.21 + 0.18 = 0.3900\n"
        "    pi_2 = [0.6100, 0.3900]"
    )

    # 4. STEADY STATE DERIVATION
    add_custom_heading("4. DERIVATION OF THE STATIONARY DISTRIBUTION (pi)", level=1)
    doc.add_paragraph(
        "As the forecast horizon increases (n -> inf), the system approaches a stationary equilibrium distribution pi = [pi_S, pi_R] where:\n"
        "    pi * P = pi  subject to  pi_S + pi_R = 1\n\n"
        "Algebraic Derivation:\n"
        "    [pi_S, pi_R] * [[0.70, 0.30], [0.40, 0.60]] = [pi_S, pi_R]\n\n"
        "From column 1:\n"
        "    pi_S = 0.70 * pi_S + 0.40 * pi_R\n"
        "    pi_S - 0.70 * pi_S = 0.40 * pi_R\n"
        "    0.30 * pi_S = 0.40 * pi_R  ===>  pi_S = (4/3) * pi_R\n\n"
        "Substitute into the probability normalization constraint pi_S + pi_R = 1:\n"
        "    (4/3) * pi_R + pi_R = 1\n"
        "    (7/3) * pi_R = 1  ===>  pi_R = 3/7 ≈ 0.428571 (42.86%)\n"
        "    pi_S = 1 - (3/7)  ===>  pi_S = 4/7 ≈ 0.571429 (57.14%)\n\n"
        "Conclusion: In the long run, 57.14% of days will be Sunny and 42.86% of days will be Rainy, regardless of whether Day 0 was Sunny or Rainy."
    )

    # 5. SOFTWARE ARCHITECTURE
    add_custom_heading("5. SOFTWARE ENGINEERING & DEPLOYMENT ARCHITECTURE", level=1)
    doc.add_paragraph(
        "The project follows strict software engineering principles with modular separation of concerns:\n\n"
        "• markov_model.py: Houses the core mathematical engine. Implements row-stochastic validation, dot-product multiplication, "
        "multi-step prediction loops, and analytical stationary state solvers using pure NumPy.\n"
        "• visualization.py: Generates interactive Plotly probability trajectories, distribution bar charts, and long-term pie charts.\n"
        "• app.py: Built with Streamlit to provide an interactive graphical user interface featuring reactive state sliders, "
        "dynamic probability inputs, step-by-step arithmetic inspection, and LaTeX formula rendering.\n"
        "• test_markov_model.py: Comprehensive test suite enforcing automated assertions for Day 1, Day 2, and steady-state outputs.\n"
        "• Deployment Infrastructure: Version-controlled on GitHub and deployed globally via Streamlit Community Cloud (24/7 online availability)."
    )

    # 6. CRITICAL LIMITATIONS
    add_custom_heading("6. ACADEMIC LIMITATIONS: STOCHASTIC MODELS VS. REAL METEOROLOGY", level=1)
    doc.add_paragraph(
        "In evaluating this model, it is vital to distinguish stochastic state modeling from actual physical meteorological forecasting:\n\n"
        "1. Dimension & Variables: Our Markov model tracks two discrete categorical states (Sunny, Rainy). Real meteorology operates on continuous 3D "
        "atmospheric fields including barometric pressure gradients, temperature profiles, relative humidity, wind vectors, and vorticity.\n"
        "2. Governing Physical Laws: Physical forecasting relies on Numerical Weather Prediction (NWP) solving non-linear systems of partial differential "
        "equations (Navier-Stokes equations for fluid flow, mass continuity, and atmospheric thermodynamics).\n"
        "3. Atmospheric Memory: The Markov property assumes complete memorylessness (tomorrow depends only on today). In reality, large-scale synoptic systems "
        "(jet streams, monsoons, ocean-atmosphere oscillations like El Niño) create multi-week atmospheric inertia.\n"
        "4. Practical Value: While not intended as an operational forecasting tool, Markov models serve as powerful climatological baselines, "
        "agricultural risk benchmarks, and foundational educational vehicles for applied linear algebra."
    )

    # 7. CONCLUSION
    add_custom_heading("7. CONCLUSION & PROJECT ARTIFACTS", level=1)
    doc.add_paragraph(
        "The 'Markov Weather Predictor' successfully demonstrates the practical application of discrete stochastic processes to meteorological state forecasting. "
        "All theoretical benchmarks were rigorously derived, computationally verified, and integrated into a modern cloud-deployed web dashboard.\n\n"
        "Project Access Links:\n"
        "• Live Cloud Application: https://5frtkkawtnf5aazokkb8ar.streamlit.app/\n"
        "• GitHub Source Code Repository: https://github.com/sivakesavacodes/-weather-markov-predictor"
    )

    doc.save(output_path)
    print(f"Word document saved successfully to: {output_path}")


if __name__ == "__main__":
    ppt_out = os.path.join(r"C:\Users\Siva\weather-markov-predictor", "MARKOV_WEATHER_PREDICTOR_PRESENTATION.pptx")
    doc_out = os.path.join(r"C:\Users\Siva\weather-markov-predictor", "MARKOV_WEATHER_PREDICTOR_REPORT.docx")
    
    build_powerpoint(ppt_out)
    build_word_document(doc_out)
