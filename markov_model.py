"""
markov_model.py
=============================================================================
MARKOV WEATHER PREDICTOR - MATHEMATICAL CORE ENGINE

This module implements the mathematical foundations of Discrete-Time
Markov Chains (DTMC) applied to weather prediction.

Mathematical Concepts Implemented:
1. State Space: S = {Sunny, Rainy}
2. Conditional Probability & Transition Probabilities:
   P(X_{t+1} = j | X_t = i)
3. Transition Probability Matrix P (Row-stochastic verification: sum(row) == 1)
4. Markov Property:
   P(X_{t+1} | X_t, X_{t-1}, ..., X_0) = P(X_{t+1} | X_t)
5. Multi-Step Probability Forecasting:
   pi_n = pi_0 * P^n
6. Stationary / Steady-State Distribution:
   pi * P = pi  subject to  sum(pi_i) = 1
=============================================================================
"""

import numpy as np
from typing import List, Tuple, Dict


# Define the weather states
STATES = ["Sunny", "Rainy"]

# Default Transition Probability Matrix defined in the project specification:
# P = [[P(Sunny|Sunny), P(Rainy|Sunny)],
#      [P(Sunny|Rainy), P(Rainy|Rainy)]]
DEFAULT_TRANSITION_MATRIX = np.array([
    [0.7, 0.3],  # Row 0: Given Sunny today -> 70% Sunny tomorrow, 30% Rainy tomorrow
    [0.4, 0.6]   # Row 1: Given Rainy today -> 40% Sunny tomorrow, 60% Rainy tomorrow
], dtype=np.float64)


def validate_transition_matrix(matrix: np.ndarray) -> Tuple[bool, str]:
    """
    Validates whether a 2D matrix is a valid row-stochastic transition matrix.
    
    Mathematical Rules:
    1. Must be a square matrix (N x N).
    2. Every probability must be non-negative: P_ij >= 0.
    3. Every row must sum exactly to 1: sum_j(P_ij) = 1 for all i.
    
    Returns:
        (is_valid: bool, message: str)
    """
    matrix = np.array(matrix, dtype=np.float64)
    
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return False, "Matrix must be a square 2D array (N x N)."
    
    if np.any(matrix < 0.0) or np.any(matrix > 1.0):
        return False, "All probability values must be between 0.0 and 1.0."
    
    row_sums = matrix.sum(axis=1)
    if not np.allclose(row_sums, 1.0, atol=1e-5):
        return False, f"Every row must sum to 1.0. Found row sums: {row_sums}."
    
    return True, "Transition matrix is valid and row-stochastic."


def predict_next_day(current_distribution: np.ndarray, transition_matrix: np.ndarray) -> np.ndarray:
    """
    Calculates the probability distribution for the next day (Day t+1)
    using vector-matrix multiplication.
    
    Mathematical Formula:
        pi_{t+1} = pi_t * P
        
    Step-by-step arithmetic for 2 states:
        pi_{t+1, Sunny} = pi_{t, Sunny} * P[0,0] + pi_{t, Rainy} * P[1,0]
        pi_{t+1, Rainy} = pi_{t, Sunny} * P[0,1] + pi_{t, Rainy} * P[1,1]
    """
    pi_t = np.array(current_distribution, dtype=np.float64)
    P = np.array(transition_matrix, dtype=np.float64)
    
    # Vector-matrix dot product using NumPy: pi_{t+1} = pi_t @ P
    pi_next = np.dot(pi_t, P)
    
    # Ensure probabilities strictly sum to 1.0 to eliminate float precision drift
    pi_next = pi_next / np.sum(pi_next)
    return pi_next


def predict_n_days(initial_distribution: np.ndarray,
                   transition_matrix: np.ndarray,
                   n_days: int) -> List[Dict[str, float]]:
    """
    Forecasts weather probabilities day-by-day from Day 0 up to Day N.
    
    Mathematical Formulation:
        pi_0 = initial state vector (e.g., [1.0, 0.0] if today is Sunny)
        pi_1 = pi_0 * P
        pi_2 = pi_1 * P = pi_0 * P^2
        ...
        pi_n = pi_0 * P^n
        
    Returns:
        List of dictionaries with Day index, Sunny probability, and Rainy probability.
    """
    pi_current = np.array(initial_distribution, dtype=np.float64)
    P = np.array(transition_matrix, dtype=np.float64)
    
    history = []
    
    # Day 0 (Initial condition)
    history.append({
        "Day": 0,
        "Sunny": float(pi_current[0]),
        "Rainy": float(pi_current[1]),
        "Sunny_Percent": float(pi_current[0] * 100),
        "Rainy_Percent": float(pi_current[1] * 100)
    })
    
    # Iterative forward matrix multiplication
    for day in range(1, n_days + 1):
        pi_current = predict_next_day(pi_current, P)
        history.append({
            "Day": day,
            "Sunny": float(pi_current[0]),
            "Rainy": float(pi_current[1]),
            "Sunny_Percent": float(pi_current[0] * 100),
            "Rainy_Percent": float(pi_current[1] * 100)
        })
        
    return history


def compute_steady_state_analytical(transition_matrix: np.ndarray) -> np.ndarray:
    """
    Computes the exact long-term stationary distribution pi = [pi_S, pi_R]
    using the algebraic closed-form formula for a 2-state Markov chain.
    
    Derivation:
        Let P = [[1 - a,   a  ],
                 [  b  , 1 - b ]]
        Here:
          a = P(Rainy | Sunny) = 0.3
          b = P(Sunny | Rainy) = 0.4
          
        Stationary condition:
            pi * P = pi
            pi_S = (1 - a) * pi_S + b * pi_R
            pi_S - (1 - a) * pi_S = b * pi_R
            a * pi_S = b * pi_R  ===>  pi_S = (b / a) * pi_R
            
        Normalization condition:
            pi_S + pi_R = 1
            (b / a) * pi_R + pi_R = 1
            pi_R * (1 + b / a) = 1
            pi_R * ((a + b) / a) = 1
            
        Therefore:
            pi_R = a / (a + b) = 0.3 / (0.3 + 0.4) = 3 / 7 approx 0.428571 (42.86%)
            pi_S = b / (a + b) = 0.4 / (0.3 + 0.4) = 4 / 7 approx 0.571429 (57.14%)
    """
    P = np.array(transition_matrix, dtype=np.float64)
    a = P[0, 1]  # P(Rainy | Sunny)
    b = P[1, 0]  # P(Sunny | Rainy)
    
    denom = a + b
    if np.isclose(denom, 0.0):
        # Degenerate case where transitions between states never happen
        return np.array([0.5, 0.5], dtype=np.float64)
    
    pi_sunny = b / denom
    pi_rainy = a / denom
    return np.array([pi_sunny, pi_rainy], dtype=np.float64)


def compute_steady_state_linear_algebra(transition_matrix: np.ndarray) -> np.ndarray:
    """
    Solves for steady state using Linear Algebra (Eigenvector / Null Space method).
    
    Mathematical Formulation:
        pi * P = pi
        pi * P - pi = 0
        pi * (P - I) = 0
        (P^T - I) * pi^T = 0
        
    We replace one redundant equation with the normalization condition:
        sum(pi_i) = 1
        
    Setting up the linear system: A * pi^T = b
    """
    P = np.array(transition_matrix, dtype=np.float64)
    n = P.shape[0]
    
    # A = (P^T - I)
    A = P.T - np.eye(n)
    # Replace the last equation with sum(pi) = 1
    A[-1, :] = 1.0
    
    b = np.zeros(n)
    b[-1] = 1.0
    
    # Solve linear equations A * pi = b
    pi_steady = np.linalg.solve(A, b)
    return pi_steady


def get_step_by_step_explanation(day_num: int,
                                 pi_prev: np.ndarray,
                                 P: np.ndarray) -> Dict[str, str]:
    """
    Provides an explicit, beginner-friendly textual breakdown of the
    matrix multiplication dot-product arithmetic for educational clarity.
    """
    s_prev = pi_prev[0]
    r_prev = pi_prev[1]
    
    p_ss = P[0, 0]
    p_sr = P[0, 1]
    p_rs = P[1, 0]
    p_rr = P[1, 1]
    
    term_s1 = s_prev * p_ss
    term_s2 = r_prev * p_rs
    s_next = term_s1 + term_s2
    
    term_r1 = s_prev * p_sr
    term_r2 = r_prev * p_rr
    r_next = term_r1 + term_r2
    
    return {
        "sunny_calc": (
            f"P(Sunny on Day {day_num}) = [P(Sunny on Day {day_num-1}) × P(Sunny|Sunny)] + [P(Rainy on Day {day_num-1}) × P(Sunny|Rainy)]\n"
            f"                         = [{s_prev:.4f} × {p_ss}] + [{r_prev:.4f} × {p_rs}]\n"
            f"                         = {term_s1:.4f} + {term_s2:.4f} = {s_next:.4f} ({s_next*100:.2f}%)"
        ),
        "rainy_calc": (
            f"P(Rainy on Day {day_num}) = [P(Sunny on Day {day_num-1}) × P(Rainy|Sunny)] + [P(Rainy on Day {day_num-1}) × P(Rainy|Rainy)]\n"
            f"                         = [{s_prev:.4f} × {p_sr}] + [{r_prev:.4f} × {p_rr}]\n"
            f"                         = {term_r1:.4f} + {term_r2:.4f} = {r_next:.4f} ({r_next*100:.2f}%)"
        ),
        "sum_check": f"{s_next:.4f} + {r_next:.4f} = {s_next + r_next:.4f} (100.0%)"
    }
