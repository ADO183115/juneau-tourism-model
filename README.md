## 🚧 This project is currently under construction. More information will be added soon. 🚧

# 1. juneau-tourism-model
A multi-objective optimization model of the tourism industry in Juneau, Alaska. Implements a discrete-time state-space framework and uses Scipy's optimization library. Optimizaes taxation and investment rate while balancing objectives such as profit, environment, and resident satisfaction. Designed to identify sustainable equilibrium points.

# 2. Variables and Parameters

### **State Variables**
| Symbol | Definition | Symbol | Definition |
| :--- | :--- | :--- | :--- |
| **$T_t$** | # of tourists | **$M_t$** | Government reinvestment |
| **$E_t$** | Environmental index | **$P_t$** | Total tourism profit |
| **$Q_t$** | Resident satisfaction | **$P_{scaled,t}$** | Total tourism profit scaled |
| **$R_t$** | Revenue from tourism | **$g_t$** | Growth rate of $T$ |
| **$G_t$** | Government revenue | **$E_{sub,t}$** | Post government intervention E |

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

### **Optimization Weights**
| Target | Weights | Definition |
| :--- | :--- | :--- |
| **Resident Satisfaction $Q$** | **$\omega_1, \omega_2, \omega_3$** | Weights for $T$ volume gap, environment, and tax burden |
| **Objective Function $V$** | **$\omega_4, \omega_5, \omega_6$** | Weights for profit $P$, environment, and resident $Q$ |

# 3. Simulation Model

## Tourist Demand Model ($T$)
The number of tourists evolves based on organic growth, government investment, and the deterrent effect of taxation:\
$$T_{t+1} = T_t (1 + g_t - \gamma \tau_t)$$

> **Growth Rate ($g$):** $g_t = g_{base} + \eta \sqrt{M_t}$
>
> **Govt. Investment ($M$):** $M_t = \lambda_t \cdot G_t$
>
> **Govt. Revenue ($G$):** $G_t = \tau_t \cdot R_t$
>
> **Total Revenue ($R$):** $R_t = r \cdot T_t$

## Environmental Model ($E$)
The environmental index accounts for natural recovery and the negative impact of tourism density:\
$$E_{t+1} = E_{sub,t} + z(1 - E_{sub,t}) - h\left(\frac{T_t}{T_{max}}\right)$$

> **Mitigated State ($E_{sub,t}$):** $E_{sub,t} = E_t + \alpha \cdot M_t$

## Resident Satisfaction Model ($Q$)
Social welfare is modeled as a balance between tourist volume proximity to an optimum, environmental health, and the local tax burden:\
$$Q_t = \omega_1 \left( 1 - \frac{|T_t - T_{opt}|}{T_{opt}} \right) + \omega_2 E_t - \omega_3 \tau_t$$

## Tourism Profit Model ($P$)
Net profit after accounting for fixed infrastructure and variable operational costs:\
$$P_t = R_t - (C_{fixed} + C_{variable} \cdot T_t)$$

## Global Objective Function ($V$)
The optimizer seeks to maximize the weighted sum of profit, environment, and satisfaction over the entire simulation horizon:\
$$V = \sum_{t=1}^{Y} \left( \omega_4 P_{scaled,t} + \omega_5 E_t + \omega_6 Q_t \right)$$

# 4. Interpretations
The goal of this model was to simulate the tourism indsutry of Juneau, Alaska for the next 5 years. The following is the data the model outputs:
|   Year |       T |        E |        Q |       P |        V |
|-------:|--------:|---------:|---------:|--------:|---------:|
|      1 | 1.67    | 0.5      | 0.97472  | 69.9001 | 0.884832 |
|      2 | 1.70464 | 0.721667 | 0.996712 | 75.499  | 0.95838  |
|      3 | 1.73426 | 0.715893 | 0.973737 | 80.2853 | 0.957135 |
|      4 | 1.75544 | 0.710957 | 0.960088 | 83.7082 | 0.957753 |
|      5 | 1.78353 | 0.707427 | 0.951349 | 88.248  | 0.964793 |

It can be seen that the model successfully balances various optimization parameters.
The aggregate system utility V changed from 0.884832 to 0.964793, an increase of 9% while the environment say an increase of over 40%!
This model is able to replicate real-life dynamics into mathematical equations, proving itself to be an effective policy-making tool.

# 5. Limitations

## Sacrifices for a Finite Horizon
While the 5-year results for T, E, Q, P, and V appear strong, the trajectories of G and M reveal the underlying costs driving those outcomes. The sharp decline observed in G and M during Year 5 is likely attributable to the model's finite horizon. Because Year 6 is outside the optimization window, the model does not prioritize G and M in order to maximize V in Year 5.

To obtain reliable values for G and M in Year 5, one recommended approach is to extend the time horizon to Y = 6. This ensures that Years 1 through 5 produce valid and stable results, while Year 6 serves as a buffer period whose outputs can be ignored.

|   Year |        G |         M |
|-------:|---------:|----------:|
|      1 | 19.114   | 16.9909   |
|      2 | 18.2802  |  9.43181  |
|      3 | 22.0487  |  9.47024  |
|      4 | 19.8648  |  9.64671  |
|      5 |  1.90992 |  0.381984 |

## Arbitrary Values for Parameters and Weights
Several parameter and weight values were not derived from real-world data. For instance, **$E_{initial}$** was set to 0.5 as a neutral midpoint on the [0.0, 1.0] index scale, given the absence of a principled method for its selection. A potential avenue for improvement would be to conduct further research to identify empirically grounded estimates for these parameters, rather than relying on arbitrary assignments. Alternatively, statistical inference methods such as maximum likelihood estimation or Bayesian inference, could be employed to derive parameter values from observed tourism data, rather than relying on arbitrary assignments.