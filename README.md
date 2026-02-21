## 🚧 This project is currently under construction. More information will be added soon. 🚧

# 1. juneau-tourism-model
A multi-objective optimization model of the tourism industry in Juneau, Alaska. Implements a discrete-time state-space framework and uses Scipy's optimization library. Optimizaes taxation and investment rate while balancing objectives such as profit, environment, and resident satisfaction. Designed to identify sustainable equilibrium points.

# 2. Variables and Parameters

### **State and Control Variables**
| Symbol | Definition | Symbol | Definition |
| :--- | :--- | :--- | :--- |
| **$T_t$** | # of tourists | **$P_t$** | Total tourism profit |
| **$E_t$** | Environmental index | **$g_t$** | Growth rate of $T$ |
| **$Q_t$** | Resident satisfaction | **$E_{sub,t}$** | Post-intervention environment |
| **$R_t$** | Revenue from tourism | **$\lambda_t$** | Investment rate (Control) |
| **$G_t$** | Government revenue | **$\tau_t$** | Tax Rate (Control) |
| **$M_t$** | Govt. investment | | |

### **Model Parameters**
| Category | Parameter | Definition |
| :--- | :--- | :--- |
| **Initial** | **$T_{initial}, E_{initial}$** | Initial tourist volume and environmental state |
| **Baselines** | **$Y, g_{base}, r$** | Simulation years, base growth, and revenue per tourist |
| **Thresholds** | **$T_{max}, T_{opt}$** | Carrying capacity and optimal satisfaction level |
| **Sensitivities** | **$\alpha, \eta, \gamma, z, h$** | Impact coefficients for $E_{sub}, g, \tau,$ recovery, and decay |
| **Costs** | **$c_{fixed}, c_{variable}$** | Fixed and variable operational costs |

### **Optimization Weights ($\omega$)**
| Target | Weights | Definition |
| :--- | :--- | :--- |
| **Satisfaction ($Q$)** | **$\omega_1, \omega_2, \omega_3$** | Weights for $T$ volume gap, environment, and tax burden |
| **Objective ($V$)** | **$\omega_4, \omega_5, \omega_6$** | Weights for profit $P$, environment, and resident $Q$ |

# 3. Simulation Model

## Tourist Demand Model **$T$**
$$T_{t+1} = T_t (1 + g_t - \gamma \tau_t)$$
### Calculate Growth Rate **$g$**
$$g_t = g_{base} + \eta \sqrt{M_t}$$
### Calcilate Government Expenditure on Tourism Development **$M$**
$$M_t = \lambda_t \cdot G_t$$
### Calculate Government Revenue from Tourism Taxation **$G$**
$$G_t = \tau_t \cdot R_t$$
### Calculate Total Tourism Revenue **$R$**
$$R_t = r \cdot T_t$$

## Environmental Model **$E$**
$$E_{t+1} = E_{sub,t} + z(1 - E_{sub,t}) - h\left(\frac{T_t}{T_{max}}\right)$$
### Calculate **$E_{sub,t}$**
$$E_{sub,t} = E_t + \alpha M_t$$

## Resident Satisfaction Model **$Q$**
$$Q_t = \omega_1 \left( 1 - \frac{|T_t - T_{opt}|}{T_{opt}} \right) + \omega_2 E_t - \omega_3 \tau_t$$

## Calculate Total Tourism Profit **$P$**
$$P_t = R_t - (C_{fixed} + C_{variable} \cdot T_t)$$

## Objective Function **$V$**
$$V = \sum_{t=1}^{Y} \left( \omega_4 \hat{P}_t + \omega_5 E_t + \omega_6 Q_t \right)$$