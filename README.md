# 🚧 This project is currently under construction. More information will be added soon. 🚧

# juneau-tourism-model
A multi-objective optimization model of the tourism industry in Juneau, Alaska. Implements a discrete-time state-space framework and uses Scipy's optimization library. Optimizaes taxation and investment rate while balancing objectives such as profit, environment, and resident satisfaction. Designed to identify sustainable equilibrium points.

# State Variables
'''T: # of tourists
E: environmental index
Q: resident satisfaction
R: revenue from tourism 
G: government revenue from R
M: government investment into tourism development
g: growth rate of T
E_sub: environmental index after applying government intervention'''

# Control Variables
lambda: investment rate into tourism industry from government revenue
tau: Tax Rate
# Parameters
Y: # of years to simulate
T_initial: # of tourists at year 0
T_max: maximum # of tourists the environment can handle without environmental degradation
T_opt: optimal # of tourists for resident satisfaction
E_initial: environmental index at year 0
g_base: base growth rate for 

alpha: sensitivity in E_sub per unit of M
eta: sensitivity of g per unit of M ** 0.5
gamma: sensitivity of of T per unit of tau
revenue_per_tourist: revenue per tourist
recovery_rate: natural recovery rate of E
h: 
omega_1
omega_2
omega_3
omega_4
omega_5
omega_6
c_fixed
c_vairable

# Simulation Model
# Tourist Demand Model
T<sub>next year</sub> = (1 * )

# Objective Function