import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_fetcher import fetch_data, SERIES_IDS
from src.modeling import fit_arima, fit_garch, forecast_volatility
from src.risk_calculator import calculate_var, calculate_es
from src.backtesting import backtest_var

# --- Page Configuration ---
st.set_page_config(
    page_title="Energy Risk Dashboard",
    page_icon="ð£ï¸",
    layout="wide"
)

# --- Helper Functions ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# --- Main Application ---
st.title("Energy Risk Forecasting Dashboard")

# --- Sidebar for User Input ---
st.sidebar.header("Settings")

# IMPORTANT: Replace with your actual FRED API key
# You can get a free key from: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = st.sidebar.text_input("FRED API Key", "YOUR_API_KEY_HERE")

selected_series = st.sidebar.selectbox(
    "Select Commodity",
    list(SERIES_IDS.keys())
)

horizon = st.sidebar.slider("Forecast Horizon (days)", 1, 30, 10)

if FRED_API_KEY != "YOUR_API_KEY_HERE":
    try:
        # --- Fetch and Display Data ---
        st.header(f"{selected_series} Price Data")
        series_id = SERIES_IDS[selected_series]
        data = fetch_data(FRED_API_KEY, series_id)

        st.line_chart(data)

        st.write("### Raw Data")
        st.dataframe(data.tail())

        # --- Modeling and Risk Calculation ---
        if st.button("Run Analysis"):
            st.header("Risk Analysis")

            # Calculate returns
            returns = data[series_id].pct_change().dropna()

            # Fit ARIMA model
            with st.spinner("Fitting ARIMA model..."):
                arima_model = fit_arima(data[series_id])
            st.success("ARIMA model fitted successfully.")

            # Fit GARCH model
            vol_model = st.sidebar.selectbox("Volatility Model", ['GARCH', 'EGARCH'])
            dist = st.sidebar.selectbox("Distribution", ['normal', 't'])
            with st.spinner("Fitting GARCH model..."):
                garch_model = fit_garch(arima_model.resid, vol=vol_model, dist=dist)
            st.success("GARCH model fitted successfully.")

            # Forecast volatility
            forecasted_vol = forecast_volatility(garch_model, horizon=horizon)

            # Calculate VaR and ES
            var_95 = calculate_var(forecasted_vol.iloc[0], garch_model.params['nu'] if dist == 't' else None)
            es_95 = calculate_es(forecasted_vol.iloc[0], garch_model.params['nu'] if dist == 't' else None)

            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Forecasted Volatility (1-day)", f"{forecasted_vol.iloc[0]:.4f}")
            col2.metric("Value-at-Risk (95%)", f"{var_95:.4f}")
            col3.metric("Expected Shortfall (95%)", f"{es_95:.4f}")

            # Plot conditional volatility
            st.subheader("Conditional Volatility")
            st.line_chart(garch_model.conditional_volatility, use_container_width=True)

            # Plot forecasted volatility
            st.subheader(f"Forecasted Volatility ({horizon} days)")
            forecast_df = pd.DataFrame({'Day': range(1, horizon + 1), 'Forecasted Volatility': forecasted_vol.values})
            st.markdown(forecast_df.to_html(index=False), unsafe_allow_html=True)
            
            import altair as alt
            chart = alt.Chart(forecast_df).mark_line().encode(
                x='Day',
                y=alt.Y('Forecasted Volatility', scale=alt.Scale(domain=[forecast_df['Forecasted Volatility'].min() * 0.99, forecast_df['Forecasted Volatility'].max() * 1.01]))
            )
            st.altair_chart(chart, use_container_width=True)

            # --- Backtesting ---
            st.header("VaR Backtesting")
            
            aligned_returns, aligned_vol = returns.align(garch_model.conditional_volatility, join='inner')
            
            exceptions, historical_var = backtest_var(aligned_returns, aligned_vol, garch_model.params['nu'] if dist == 't' else None)
            st.metric("Number of Exceptions", f"{exceptions} (Expected: {int(len(aligned_returns) * 0.05)})")

            # Plot backtesting results
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=returns.index, y=returns, mode='lines', name='Returns'))
            fig.add_trace(go.Scatter(x=historical_var.index, y=historical_var, mode='lines', name='VaR', line=dict(color='red')))
            st.plotly_chart(fig, use_container_width=True)

            # --- Download Report ---
            st.header("Download Report")
            report_df = pd.DataFrame({
                "Returns": returns,
                "Conditional Volatility": garch_model.conditional_volatility,
                "VaR (95%)": historical_var
            })
            csv = convert_df_to_csv(report_df)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{selected_series}_risk_report.csv",
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your FRED API key in the sidebar to fetch data.")
