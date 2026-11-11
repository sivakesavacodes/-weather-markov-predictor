"""
test_markov_model.py
=============================================================================
Validation script for Markov Weather Predictor mathematical model.
Tests all benchmark criteria against the presentation requirements.
=============================================================================
"""

import numpy as np
from markov_model import (
    DEFAULT_TRANSITION_MATRIX,
    validate_transition_matrix,
    predict_next_day,
    predict_n_days,
    compute_steady_state_analytical,
    compute_steady_state_linear_algebra,
    get_step_by_step_explanation
)


def run_tests():
    print("=" * 70)
    print("STARTING MARKOV MODEL MATHEMATICAL VALIDATION")
    print("=" * 70)
    
    # 1. Validate Transition Matrix properties
    print("\n[TEST 1] Validating Transition Matrix P:")
    print(DEFAULT_TRANSITION_MATRIX)
    is_valid, msg = validate_transition_matrix(DEFAULT_TRANSITION_MATRIX)
    assert is_valid, f"Validation failed: {msg}"
    print("✓ Matrix is a valid 2x2 row-stochastic matrix.")
    print("  Row 0 sum (Sunny):", np.sum(DEFAULT_TRANSITION_MATRIX[0, :]))
    print("  Row 1 sum (Rainy):", np.sum(DEFAULT_TRANSITION_MATRIX[1, :]))
    
    # 2. Initial state setup: pi_0 = [1.0, 0.0]
    pi_0 = np.array([1.0, 0.0])
    print("\n[TEST 2] Initial State Distribution (pi_0):")
    print(f"  Today is 100% Sunny: pi_0 = {pi_0}")
    assert np.allclose(pi_0, [1.0, 0.0])
    
    # 3. Forecast Day 1: Expected pi_1 = [0.7, 0.3]
    pi_1 = predict_next_day(pi_0, DEFAULT_TRANSITION_MATRIX)
    print("\n[TEST 3] Day 1 Forecast:")
    print(f"  Calculated pi_1: {pi_1}")
    print(f"  Sunny: {pi_1[0]*100:.2f}%, Rainy: {pi_1[1]*100:.2f}%")
    assert np.allclose(pi_1, [0.7, 0.3], atol=1e-5), f"Day 1 mismatch: got {pi_1}"
    print("✓ Day 1 matches expected [0.7, 0.3] (70% Sunny, 30% Rainy).")
    
    # 4. Forecast Day 2: Expected pi_2 = [0.61, 0.39]
    pi_2 = predict_next_day(pi_1, DEFAULT_TRANSITION_MATRIX)
    print("\n[TEST 4] Day 2 Forecast:")
    print(f"  Calculated pi_2: {pi_2}")
    print(f"  Sunny: {pi_2[0]*100:.2f}%, Rainy: {pi_2[1]*100:.2f}%")
    assert np.allclose(pi_2, [0.61, 0.39], atol=1e-5), f"Day 2 mismatch: got {pi_2}"
    print("✓ Day 2 matches expected [0.61, 0.39] (61% Sunny, 39% Rainy).")
    
    # 5. Predict N Days sequence
    forecast = predict_n_days(pi_0, DEFAULT_TRANSITION_MATRIX, n_days=5)
    print("\n[TEST 5] 5-Day Trajectory:")
    for row in forecast:
        print(f"  Day {row['Day']}: Sunny = {row['Sunny_Percent']:6.2f}%, Rainy = {row['Rainy_Percent']:6.2f}%")
        assert np.isclose(row['Sunny'] + row['Rainy'], 1.0)
    print("✓ All probabilities sum to 1.0 across all days.")
    
    # 6. Steady-State Calculation
    pi_steady_analytical = compute_steady_state_analytical(DEFAULT_TRANSITION_MATRIX)
    pi_steady_linalg = compute_steady_state_linear_algebra(DEFAULT_TRANSITION_MATRIX)
    
    print("\n[TEST 6] Steady-State Distribution (pi):")
    print(f"  Analytical:   Sunny = {pi_steady_analytical[0]:.4f} ({pi_steady_analytical[0]*100:.2f}%), "
          f"Rainy = {pi_steady_analytical[1]:.4f} ({pi_steady_analytical[1]*100:.2f}%)")
    print(f"  Linear Alg:   Sunny = {pi_steady_linalg[0]:.4f} ({pi_steady_linalg[0]*100:.2f}%), "
          f"Rainy = {pi_steady_linalg[1]:.4f} ({pi_steady_linalg[1]*100:.2f}%)")
    
    expected_steady = np.array([4.0 / 7.0, 3.0 / 7.0])  # ~ [0.571428..., 0.428571...]
    assert np.allclose(pi_steady_analytical, expected_steady, atol=1e-4)
    assert np.allclose(pi_steady_linalg, expected_steady, atol=1e-4)
    print("✓ Steady state matches expected [0.5714, 0.4286] (4/7 Sunny, 3/7 Rainy).")
    
    # 7. Check Invariance property: pi_steady * P == pi_steady
    invariance_check = np.dot(pi_steady_analytical, DEFAULT_TRANSITION_MATRIX)
    assert np.allclose(invariance_check, pi_steady_analytical, atol=1e-5)
    print("✓ Invariance property verified: pi * P = pi.")
    
    # 8. Step-by-Step Educational Explanation Test
    print("\n[TEST 8] Educational Step-by-Step Breakdown for Day 1:")
    explanation = get_step_by_step_explanation(1, pi_0, DEFAULT_TRANSITION_MATRIX)
    print(explanation['sunny_calc'])
    print(explanation['rainy_calc'])
    print("Sum check:", explanation['sum_check'])
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED PERFECTLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
