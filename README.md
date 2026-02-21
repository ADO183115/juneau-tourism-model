## 🚧 This project is currently under construction. More information will be added soon. 🚧

# juneau-tourism-model
A multi-objective optimization model of the tourism industry in Juneau, Alaska. Implements a discrete-time state-space framework and uses Scipy's optimization library. Optimizaes taxation and investment rate while balancing objectives such as profit, environment, and resident satisfaction. Designed to identify sustainable equilibrium points.

# Variables and Parameters
## State Variables
T: # of tourists\
E: environmental index\
Q: resident satisfaction\
R: revenue from tourism \
G: government revenue from R\
M: government investment into tourism development\
P: total tourism profit after operating costs\
g: growth rate of T\
E_sub: environmental index after applying government intervention

## Control Variables
lambda: investment rate into tourism industry from government revenue\
tau: Tax Rate

## Parameters
Y: # of years to simulate\
T_initial: # of tourists at year 0\
T_max: maximum # of tourists the environment can handle without environmental degradation\
T_opt: optimal # of tourists for resident satisfaction\
E_initial: environmental index at year 0\
g_base: base growth rate for # of tourists\
\
alpha: sensitivity of E_sub per unit of M\
eta: sensitivity of g per unit of M ** 0.5\
gamma: sensitivity of of T per unit of tau\
r: revenue per tourist\
z: natural recovery rate of E\
h: sensitivity of E per unit of carrying capacity utilization\
c_fixed: fixed operational cost\
c_vairable: variable operational cost scaling with T\
\
omega_1: weight assigned to optimal tourists level when calculating Q\
omega_2: weight assigned to environmental index when calculating Q\
omega_3: weight assiged to taxation when calculating Q\
\
omega_4: weight assigned to profit scaled when calculating V\
omega_5: weight assigned to environmental index when calculating V\
omega_6: weight assigned to resident satisfaction when calculating V

# Simulation Model
## Tourist Demand Model T
$$T_{t+1} = T_t (1 + g_t - \gamma \tau_t)$$

## Environmental Model E
$$E_{t+1} = E_{sub,t} + z(1 - E_{sub,t}) - h\left(\frac{T_t}{T_{max}}\right)$$\
$$E_{sub,t} = E_t + \alpha M_t$$

## Resident Satisfaction Model Q
$$Q_t = \omega_1 \left( 1 - \frac{|T_t - T_{opt}|}{T_{opt}} \right) + \omega_2 E_t - \omega_3 \tau_t$$

## Calculate Growth Rate g
$$g_t = g_{base} + \eta \sqrt{M_t}$$

## Calculate Total Tourism Revenue R
$$R_t = r \cdot T_t$$

## Calculate Government Revenue from Tourism Taxation G
$$G_t = \tau_t \cdot R_t$$

## Calcilate Government Expenditure on Tourism Development M
$$M_t = \lambda_t \cdot G_t$$

## Calculate Total Tourism Profit P
$$P_t = R_t - (C_{fixed} + C_{variable} \cdot T_t)$$

## Objective Function
$$V = \sum_{t=1}^{Y} \left( \omega_4 \hat{P}_t + \omega_5 E_t + \omega_6 Q_t \right)$$