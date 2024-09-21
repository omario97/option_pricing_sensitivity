import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go


# Add creator info and social links to the sidebar
st.sidebar.markdown("<h3 style='text-align: left; color: #888888;'>Created by Omar Hussain</h3>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="display: flex; justify-content: left; align-items: center;">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <a href="https://www.linkedin.com/in/omar-hussain-504777164/" target="_blank" style="text-decoration: none; color: inherit; margin-right: 20px;">
        <i class="fab fa-linkedin" style="font-size: 24px;"></i>
    </a>
    <a href="https://github.com/omario97" target="_blank" style="text-decoration: none; color: inherit;">
        <i class="fab fa-github" style="font-size: 24px;"></i>
    </a>
</div>
""", unsafe_allow_html=True)


# Black-Scholes function (copy this from your main app)
def black_scholes(S0, K, T, r, sigma, option_type):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

# Sidebar inputs
st.sidebar.header("Option Parameters")
S0 = st.sidebar.number_input("Initial Stock Price (S0)", min_value=1.0, value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=100.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (T) in years", min_value=1, value=1, step=1)
r = st.sidebar.number_input("Risk-free Rate (r)", min_value=0.0, value=0.05, step=0.01)
sigma = st.sidebar.number_input("Volatility (σ)", min_value=0.01, value=0.2, step=0.01)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

# Sensitivity analysis
st.header("Sensitivity Analysis")

st.markdown("*Source code available on my [GitHub](https://github.com/omario97) page*")


sensitivity_param = st.selectbox("Select parameter for sensitivity analysis", 
                                 ["Volatility", "Strike Price", "Time to Maturity", "Initial Stock Price"])

if sensitivity_param == "Volatility":
    range_values = np.linspace(max(0.05, sigma-0.2), sigma+0.2, 20)
    prices = [black_scholes(S0, K, T, r, vol, option_type) for vol in range_values]
    x_label = "Volatility"
elif sensitivity_param == "Strike Price":
    range_values = np.linspace(max(1, K-50), K+50, 20)
    prices = [black_scholes(S0, k, T, r, sigma, option_type) for k in range_values]
    x_label = "Strike Price"
elif sensitivity_param == "Time to Maturity":
    range_values = np.linspace(max(0.1, T-2), T+2, 20)
    prices = [black_scholes(S0, K, t, r, sigma, option_type) for t in range_values]
    x_label = "Time to Maturity (Years)"
else:  # Initial Stock Price
    range_values = np.linspace(max(1, S0-50), S0+50, 20)
    prices = [black_scholes(s, K, T, r, sigma, option_type) for s in range_values]
    x_label = "Initial Stock Price"

fig = go.Figure()
fig.add_trace(go.Scatter(x=range_values, y=prices, mode='lines+markers'))
fig.update_layout(title=f"Sensitivity to {sensitivity_param}",
                  xaxis_title=x_label,
                  yaxis_title="Option Price")
st.plotly_chart(fig)

# Display current option price
current_price = black_scholes(S0, K, T, r, sigma, option_type)
st.write(f"Current {option_type} option price: ${current_price:.2f}")

# Explanation
st.header("How to Interpret")
st.write("""
This sensitivity analysis shows how the option price changes when we vary one parameter while keeping all others constant. 
The graph illustrates the relationship between the selected parameter and the option price. 
A steeper line indicates that the option price is more sensitive to changes in that parameter.

- Volatility: Higher volatility typically increases option prices for both calls and puts.
- Strike Price: For call options, price decreases as strike price increases. For put options, it's the opposite.
- Time to Maturity: The effect can vary based on whether the option is in-the-money or out-of-the-money.
- Initial Stock Price: Call options increase in value as the stock price increases, while put options decrease.
""")