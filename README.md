## 🚧 This project is currently under construction. More information will be added soon. 🚧

# 1. juneau-tourism-model
A multi-objective optimization model of the tourism industry in Juneau, Alaska. Implements a discrete-time state-space framework and uses Scipy's optimization library. Optimizaes taxation and investment rate while balancing objectives such as profit, environment, and resident satisfaction. Designed to identify sustainable equilibrium points.

# 2. Variables and Parameters

### **State Variables**
| Symbol | Definition | Symbol | Definition |
| :--- | :--- | :--- | :--- |
| **$T_t$** | # of tourists | **$M_t$** | Government investment |
| **$E_t$** | Environmental index | **$P_t$** | Total tourism profit |
| **$Q_t$** | Resident satisfaction | **$g_t$** | Growth rate of $T$ |
| **$R_t$** | Revenue from tourism | **$E_{sub,t}$** | Post government intervention E |
| **$G_t$** | Government revenue | | |

### **Control Variables**
| Symbol | Definition |
| :--- | :--- |
|**$\lambda_t$** | Investment rate |
| **$\tau_t$** | Tax Rate |

### **Model Parameters**
| Category | Parameter | Definition |
| :--- | :--- | :--- |
| **Initial** | **$T_{initial}, E_{initial}$** | Initial tourist volume and environmental state |
| **Baselines** | **$Y, g_{base}, r$** | Simulation years, base growth, and revenue per tourist |
| **Thresholds** | **$T_{max}, T_{opt}$** | Carrying capacity and optimal satisfaction level |
| **Sensitivities** | **$\alpha, \eta, \gamma, z, h$** | Impact/sensitivity coefficients |
| **Costs** | **$c_{fixed}, c_{variable}$** | Fixed and variable tourism operational costs |

### **Optimization Weights ($\omega$)**
| Target | Weights | Definition |
| :--- | :--- | :--- |
| **Resident Satisfaction $Q$** | **$\omega_1, \omega_2, \omega_3$** | Weights for $T$ volume gap, environment, and tax burden |
| **Objective Function $V$** | **$\omega_4, \omega_5, \omega_6$** | Weights for profit $P$, environment, and resident $Q$ |

# 3. Simulation Model

---

## ✈️ Tourist Demand Model ($T$)
The number of tourists evolves based on organic growth, government investment, and the deterrent effect of taxation:
$$T_{t+1} = T_t (1 + g_t - \gamma \tau_t)$$

> **Sub-calculations:**
> * **Growth Rate ($g$):** $g_t = g_{base} + \eta \sqrt{M_t}$
> * **Govt. Investment ($M$):** $M_t = \lambda_t \cdot G_t$
> * **Govt. Revenue ($G$):** $G_t = \tau_t \cdot R_t$
> * **Total Revenue ($R$):** $R_t = r \cdot T_t$

---

## 🌲 Environmental Model ($E$)
The environmental index accounts for natural recovery and the negative impact of tourism density:
$$E_{t+1} = E_{sub,t} + z(1 - E_{sub,t}) - h\left(\frac{T_t}{T_{max}}\right)$$

> **Sub-calculation:**
> * **Mitigated State ($E_{sub,t}$):** $E_{sub,t} = E_t + \alpha M_t$

---

## 🤝 Resident Satisfaction Model ($Q$)
Social welfare is modeled as a balance between tourist volume proximity to an optimum, environmental health, and the local tax burden:
$$Q_t = \omega_1 \left( 1 - \frac{|T_t - T_{opt}|}{T_{opt}} \right) + \omega_2 E_t - \omega_3 \tau_t$$

---

## 💰 Tourism Profit Model ($P$)
Net profit after accounting for fixed infrastructure and variable operational costs:
$$P_t = R_t - (C_{fixed} + C_{variable} \cdot T_t)$$

---

## 🎯 Global Objective Function ($V$)
The optimizer seeks to maximize the weighted sum of profit, environment, and satisfaction over the entire simulation horizon:
$$V = \sum_{t=1}^{Y} \left( \omega_4 \hat{P}_t + \omega_5 E_t + \omega_6 Q_t \right)$$