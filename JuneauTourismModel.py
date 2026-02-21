import numpy as np
import pandas as pd
from scipy.optimize import minimize
from tabulate import tabulate

# --- 1. Model Definitions ---

# Model 1: Tourist Demand
def update_T(T_t, g_t_future, gamma, tau):
    return T_t * (1 + g_t_future - gamma * tau)

# Model 2: Environmental Impact
def update_E(E_sub_t, z, h, T_t, T_max):
    return E_sub_t + z * (1 - E_sub_t) - h * (T_t / T_max)

# Model 3: Resident Satisfaction
def calculate_Q(omega_1, T_t, T_opt, omega_2, E_t, omega_3, tau):
    val = omega_1 * (1 - (abs(T_t - T_opt) / T_opt)) + omega_2 * E_t - omega_3 * tau
    return np.clip(val, 0.0, 1.0)

# Calculate growth rate g
def calculate_g(g_base, eta, M_t):
    return g_base + eta * (M_t ** 0.5)

# Calculate total tourism revenue R
def calculate_R(r, T_t):
    return r * T_t

# Calculate government revenue from tourism taxation G
def calculate_G(tau, R_t):
    return tau * R_t

# Calculate government expenditure on tourism development M
def calculate_M(lambd, G_t):
    return lambd * G_t

# Calculate improved environmental index after applying government intervention E_sub
def calculate_E_sub(E_t, alpha, M_t):
    val = E_t + alpha * M_t
    return np.clip(val, 0.0, 1.0)

# Calculate total tourism profit P
def calculate_P(R_t, c_fixed, c_variable, T_t):
    return R_t - (c_fixed + c_variable * T_t)

# Calculate optimization value V
def calculate_V(omega_4, P_scaled_t, omega_5, E_t, omega_6, Q_t):
    return np.sum(omega_4 * P_scaled_t + omega_5 * E_t + omega_6 * Q_t)

# --- 2. Parameters ---

params = {
    "Y" : 5,
    "T_initial" : 1.67, # Given
    "T_max" : 1.2, "T_opt" : 1.5, # Assumed
    "E_initial" : 0.5, # Assumed that environment is at 50% of optimal point
    "g_base" : 0.03, # Assumed
    "alpha" : 0.03, "eta" : 0.005, "gamma" : 0.5, # Assumed
    "r" : 191.6168, # Calculated
    "z" : 0.005, # Assumed
    "h" : 0.2, # Assumed
    "omega_1" : 1.0, "omega_2" : 0.2, "omega_3" : 0.2, # Assumed
    "omega_4" : 0.2, "omega_5" : 0.2, "omega_6" : 0.6, # Assumed
    "c_fixed" : 200,
    "c_variable" : 30
}

# --- 3. The Simulation Engine ---

def run_simulation(controls, params):

    # Set values
    Y = params["Y"]

    tau_t = controls[:Y]
    lambd_t = controls[Y:]

    T_t = np.zeros(Y)
    E_t = np.zeros(Y)
    Q_t = np.zeros(Y)
    P_t = np.zeros(Y)

    E_sub_t = np.zeros(Y)
    R_t = np.zeros(Y)
    G_t = np.zeros(Y)
    M_t = np.zeros(Y)
    g_t = np.zeros(Y)
    P_scaled_t = np.zeros(Y)

    V_t = np.zeros(Y)

    T = params["T_initial"]
    E = params["E_initial"]

    # Run the model for the amount of years that need to be calculated
    for t in range(Y):
        tau = tau_t[t]
        lambd = lambd_t[t]
        
        # Tourism Model
        R = calculate_R(params["r"], T)
        G = calculate_G(tau, R)
        M = calculate_M(lambd, G)

        # Environmental Model
        E_sub = calculate_E_sub(E, params["alpha"], M)

        # Resident Satisfaction Model
        Q = calculate_Q(params["omega_1"], T, params["T_opt"], params["omega_2"], E, params["omega_3"], tau)

        # Other Metrics
        P = calculate_P(R, params["c_fixed"], params["c_variable"], T)
        g = calculate_g(params["g_base"], params["eta"], M)

        # Store States
        T_t[t] = T
        E_t[t] = E

        Q_t[t] = Q
        P_t[t] = P

        E_sub_t[t] = E_sub
        R_t[t] = R
        G_t[t] = G
        M_t[t] = M
        g_t[t] = g
        P_scaled_t[t] = P_t[t] / P_t[0]

        # Calculate Optimization Value
        V_t[t] = calculate_V(params["omega_4"], P_scaled_t[t], params["omega_5"], E, params["omega_6"], Q)

        # Calculate Next Step
        T = update_T(T, g, params["gamma"], tau)
        E = update_E(E_sub, params["z"], params["h"], T_t[t], params["T_max"])

    return T_t, E_t, Q_t, P_t, E_sub_t, R_t, G_t, M_t, g_t, P_scaled_t, V_t

# --- 4. The Objective Function ---

def objective_function(controls, params):
    # In order to calculate V, must run the simulation first
    T_t, E_t, Q_t, P_t, E_sub_t, R_t, G_t, M_t, g_t, P_scaled_t, V_t = run_simulation(controls, params)

    # Cumulative optimization
    V = np.sum(V_t)

    return -V

# --- 5. Optimization ---

Y = params["Y"]

# Initial Guess (start with 5% tax and 20% investment)
initial_guess = np.concatenate([np.ones(Y) * 0.05, np.ones(Y) * 0.2])

# Bounds: Tau (0, 1), Lambda (0, 1)
bounds = [(0.0, 1.0)] * (2 * Y)

# Simulate and optimize the model
# Will return control variable values that output the maximum optimization value V over Y years
print("Optimizing...")
result = minimize(objective_function, initial_guess, args=(params,), method="L-BFGS-B", bounds=bounds)

if result.success:
    print("Optimization Successful!")
    optimal_controls = result.x
    tau_opt = optimal_controls[:Y]
    lambd_opt = optimal_controls[Y:]
    
    # Run one last time to get the data for printing
    T_fin, E_fin, Q_fin, P_fin, E_sub_fin, R_fin, G_fin, M_fin, g_fin, P_scaled_fin, V_fin = run_simulation(optimal_controls, params)

    data = [[t+1, T_fin[t], E_fin[t], R_fin[t], P_fin[t], Q_fin[t], V_fin[t]] for t in range(Y)]
    headers = ["Year", "Tourists T", "Environment E", "Revenue R", "Profit P", "Resident Satisfaction Q", "Optimization Value V"]
    print(tabulate(data, headers=headers, tablefmt="grid", floatfmt=".4f"))

    data = [[t+1, tau_opt[t], lambd_opt[t], G_fin[t], M_fin[t], E_sub_fin[t], g_fin[t], P_scaled_fin[t]] for t in range(Y)]
    headers = ["Year", "tau", "lambda", "Government Revenue from Tax G", "Government Expenditure on Tourism M", "E_sub_t", "g", "P_scaled"]
    print(tabulate(data, headers=headers, tablefmt="grid", floatfmt=".4f"))
else:
    print("Optimization Failed:", result.message)

# Saving results from the simulation to a .csv
results = {
    "Year": list(range(1, Y + 1)),
    "T": T_fin, "E": E_fin, "E_sub": E_sub_fin, "Q": Q_fin, "R": R_fin, "P": P_fin,
    "P_scaled": P_scaled_fin, "G": G_fin, "M": M_fin, "g": g_fin, "V": V_fin
}

df = pd.DataFrame(results)
df.to_csv("simulation_results.csv", index =False)