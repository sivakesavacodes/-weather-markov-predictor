# MARKOV WEATHER PREDICTOR – A STOCHASTIC PROCESS FOR WEATHER PREDICTION

An interactive Python application demonstrating how **Discrete-Time Markov Chains (DTMC)** and probability theory are used to model and predict weather state transitions.

---

## 1. Project Overview
This project models daily weather transitions between two discrete states:
* **Sunny ($S$)**
* **Rainy ($R$)**

Using a $2 \times 2$ stochastic transition probability matrix $P$, the application computes day-by-day probability trajectories, demonstrates the Markov memoryless property, and solves for the long-term steady-state equilibrium $\pi$.

---

## 2. Mathematical Foundation

### A. State Space
$$S = \{ \text{Sunny}, \text{Rainy} \}$$

### B. Transition Probability Matrix ($P$)
$$P = \begin{bmatrix}
P(\text{Sunny} \mid \text{Sunny}) & P(\text{Rainy} \mid \text{Sunny}) \\
P(\text{Sunny} \mid \text{Rainy}) & P(\text{Rainy} \mid \text{Rainy})
\end{bmatrix} = \begin{bmatrix}
0.7 & 0.3 \\
0.4 & 0.6
\end{bmatrix}$$

* **Row 0:** Given Sunny today $\to$ 70% chance of Sunny tomorrow, 30% chance of Rainy tomorrow.
* **Row 1:** Given Rainy today $\to$ 40% chance of Sunny tomorrow, 60% chance of Rainy tomorrow.
* **Row-Stochastic Condition:** Every row sums strictly to $1.0$: $\sum_{j} P_{ij} = 1$.

### C. The Markov Property
The future state depends **only** on the present state:
$$P(X_{t+1} \mid X_t, X_{t-1}, \dots, X_0) = P(X_{t+1} \mid X_t)$$

### D. Multi-Step Prediction
$$\mathbf{\pi}_n = \mathbf{\pi}_0 P^n$$

### E. Long-Term Steady State ($\mathbf{\pi}$)
Solving $\mathbf{\pi} P = \mathbf{\pi}$ with $\pi_S + \pi_R = 1$ yields the exact rational fractions:
$$\pi_S = \frac{4}{7} \approx 57.14\%$$
$$\pi_R = \frac{3}{7} \approx 42.86\%$$

---

## 3. Benchmark Verification
Starting with $\mathbf{\pi}_0 = [1.0, 0.0]$ (100% Sunny today):

| Day | $\mathbf{\pi}_n$ Formula | P(Sunny) | P(Rainy) | Sum |
|:---:|:---:|:---:|:---:|:---:|
| **Day 0** | $\mathbf{\pi}_0$ | 100.00% | 0.00% | 1.00 |
| **Day 1** | $\mathbf{\pi}_0 P$ | **70.00%** | **30.00%** | 1.00 |
| **Day 2** | $\mathbf{\pi}_1 P$ | **61.00%** | **39.00%** | 1.00 |
| **Day 3** | $\mathbf{\pi}_2 P$ | 58.30% | 41.70% | 1.00 |
| **Steady State** | $\lim_{n \to \infty} \mathbf{\pi}_n$ | **57.14%** | **42.86%** | 1.00 |

---

## 4. Project File Structure
```
weather-markov-predictor/
│
├── app.py                  # Interactive Streamlit dashboard
├── markov_model.py         # Pure mathematical engine (NumPy matrix operations)
├── visualization.py        # Plotly & Matplotlib chart generators
├── test_markov_model.py    # Unit tests & benchmark verification script
├── requirements.txt        # Python package dependencies
├── README.md               # Mathematical theory & documentation
│
└── data/                   # Directory reserved for data logs
```

---

## 5. How to Run

### Step 1: Run Unit Tests
To verify all mathematical calculations and assertions:
```bash
python test_markov_model.py
```

### Step 2: Launch the Interactive Dashboard
Run the Streamlit web application:
```bash
streamlit run app.py
```
Then open your browser at `http://localhost:8501`.

---

## 6. Academic Limitations
* **Stochastic vs. Physical:** This model demonstrates probabilistic state transitions, not physical fluid dynamics or Navier-Stokes atmospheric equations.
* **Atmospheric Variables:** Real weather forecasting incorporates continuous spatial parameters (pressure gradients, temperature, humidity, jet stream dynamics) rather than a discrete 2-state memoryless chain.
