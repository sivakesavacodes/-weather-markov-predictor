"""
visualization.py
=============================================================================
MARKOV WEATHER PREDICTOR - VISUALIZATION ENGINE

Generates interactive charts (Plotly) and static publication figures (Matplotlib)
for visualizing weather probability transitions, convergence, and steady-state distributions.
=============================================================================
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt


# Consistent color palette for weather states
COLOR_SUNNY = "#F59E0B"   # Warm Amber / Sun Yellow
COLOR_RAINY = "#3B82F6"   # Ocean Blue
COLOR_STEADY = "#10B981"  # Emerald Green for steady state


def plot_probability_trajectory_plotly(df: pd.DataFrame, steady_state: np.ndarray) -> go.Figure:
    """
    Creates an interactive line graph showing how Sunny and Rainy probabilities
    evolve day-by-day and asymptotically converge to the steady state.
    """
    fig = go.Figure()

    # Sunny trajectory
    fig.add_trace(go.Scatter(
        x=df["Day"],
        y=df["Sunny_Percent"],
        mode="lines+markers",
        name="P(Sunny)",
        line=dict(color=COLOR_SUNNY, width=3),
        marker=dict(size=8, symbol="circle"),
        hovertemplate="<b>Day %{x}</b><br>Sunny: %{y:.2f}%<extra></extra>"
    ))

    # Rainy trajectory
    fig.add_trace(go.Scatter(
        x=df["Day"],
        y=df["Rainy_Percent"],
        mode="lines+markers",
        name="P(Rainy)",
        line=dict(color=COLOR_RAINY, width=3),
        marker=dict(size=8, symbol="diamond"),
        hovertemplate="<b>Day %{x}</b><br>Rainy: %{y:.2f}%<extra></extra>"
    ))

    # Steady-state benchmark dashed lines
    fig.add_hline(
        y=steady_state[0] * 100,
        line_dash="dash",
        line_color=COLOR_SUNNY,
        opacity=0.6,
        annotation_text=f"Steady Sunny ({steady_state[0]*100:.2f}%)",
        annotation_position="bottom right"
    )

    fig.add_hline(
        y=steady_state[1] * 100,
        line_dash="dash",
        line_color=COLOR_RAINY,
        opacity=0.6,
        annotation_text=f"Steady Rainy ({steady_state[1]*100:.2f}%)",
        annotation_position="top right"
    )

    fig.update_layout(
        title="<b>Weather Probability Trajectory Over Time (Convergence to Steady State)</b>",
        xaxis_title="Days in Future",
        yaxis_title="Probability (%)",
        yaxis=dict(range=[0, 105], ticksuffix="%"),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


def plot_steady_state_pie_plotly(steady_state: np.ndarray) -> go.Figure:
    """
    Creates an interactive donut/pie chart displaying the long-term
    equilibrium probability distribution between Sunny and Rainy weather.
    """
    labels = ["Sunny (Long-term)", "Rainy (Long-term)"]
    values = [steady_state[0] * 100, steady_state[1] * 100]
    colors = [COLOR_SUNNY, COLOR_RAINY]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b>: %{value:.2f}%<extra></extra>"
    )])

    fig.update_layout(
        title="<b>Long-Term Steady-State Weather Distribution (π)</b>",
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )

    return fig


def plot_distribution_bar_plotly(df: pd.DataFrame, target_day: int) -> go.Figure:
    """
    Creates a bar chart comparing the probability distribution for a specific selected day.
    """
    day_row = df[df["Day"] == target_day].iloc[0]
    
    categories = ["Sunny", "Rainy"]
    probs = [day_row["Sunny_Percent"], day_row["Rainy_Percent"]]
    colors = [COLOR_SUNNY, COLOR_RAINY]

    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=probs,
        marker=dict(color=colors, line=dict(color="#333333", width=1.5)),
        text=[f"{p:.2f}%" for p in probs],
        textposition="auto"
    )])

    fig.update_layout(
        title=f"<b>Weather Probability Distribution on Day {target_day}</b>",
        xaxis_title="Weather State",
        yaxis_title="Probability (%)",
        yaxis=dict(range=[0, 105], ticksuffix="%"),
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def plot_matplotlib_summary(df: pd.DataFrame, steady_state: np.ndarray) -> plt.Figure:
    """
    Renders a 2-panel static Matplotlib figure suitable for report exports and posters.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=150)

    # Panel 1: Trajectory
    ax1.plot(df["Day"], df["Sunny_Percent"], color=COLOR_SUNNY, marker='o', linewidth=2, label="P(Sunny)")
    ax1.plot(df["Day"], df["Rainy_Percent"], color=COLOR_RAINY, marker='s', linewidth=2, label="P(Rainy)")
    ax1.axhline(steady_state[0] * 100, color=COLOR_SUNNY, linestyle="--", alpha=0.7, label=f"Steady Sunny ({steady_state[0]*100:.1f}%)")
    ax1.axhline(steady_state[1] * 100, color=COLOR_RAINY, linestyle="--", alpha=0.7, label=f"Steady Rainy ({steady_state[1]*100:.1f}%)")
    ax1.set_title("Probability Trajectory", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Probability (%)")
    ax1.set_ylim(0, 105)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="best", fontsize=9)

    # Panel 2: Steady State Pie
    ax2.pie(
        [steady_state[0], steady_state[1]],
        labels=[f"Sunny\n{steady_state[0]*100:.2f}%", f"Rainy\n{steady_state[1]*100:.2f}%"],
        colors=[COLOR_SUNNY, COLOR_RAINY],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2)
    )
    ax2.set_title("Long-Term Steady State (π)", fontsize=12, fontweight="bold")

    plt.tight_layout()
    return fig
