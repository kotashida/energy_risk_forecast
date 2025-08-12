# Energy Risk Forecasting Dashboard

## 1. Project Overview

This project is an interactive dashboard for forecasting the volatility of energy commodities (WTI crude oil and Henry Hub natural gas) and quantifying potential market risks. It utilizes time series analysis and advanced econometric models (ARIMA-GARCH/EGARCH) to provide daily risk metrics like Value-at-Risk (VaR) and Expected Shortfall (ES). The dashboard is designed to help traders, analysts, and risk managers make more informed decisions by providing a clear and intuitive interface for exploring risk.

## 2. Core Features

- **Data Ingestion:** Automatically fetches the latest WTI crude oil and Henry Hub natural gas prices from the FRED API.
- **Advanced Volatility Modeling:**
    - Fits ARIMA models to the price data to capture the underlying trend.
    - Offers a choice between GARCH and EGARCH models to forecast future volatility.
    - Allows for the selection of different distributions (Normal or Student's t) to better model the characteristics of financial returns.
- **Comprehensive Risk Calculation:** Computes daily VaR and ES based on the selected model and distribution.
- **Multi-day Forecasting:** Provides multi-day volatility forecasts with an interactive slider to select the forecast horizon.
- **Rigorous Backtesting:** Validates the accuracy of the VaR models against historical data and provides a clear interpretation of the results.
- **Interactive Dashboard:** Visualizes prices, conditional volatility, forecasted volatility, and backtesting results using interactive charts.
- **Downloadable Reports:** Allows users to download the analysis results in a CSV format.

## 3. Tech Stack

- **Language:** Python
- **Core Libraries:**
    - **Data Manipulation:** pandas
    - **Time Series Modeling:** statsmodels (for ARIMA), arch (for GARCH/EGARCH)
    - **Dashboard:** Streamlit
    - **Data Visualization:** Plotly, Altair

## 4. Installation and Usage

### Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kotashida/energy_risk_forecast
    cd energy-risk-forecast
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1.  **Get a FRED API Key:** You will need a free API key from the [FRED website](https://fred.stlouisfed.org/docs/api/api_key.html).
2.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
3.  **Enter your API Key:** Paste your FRED API key into the text box in the sidebar.
4.  **Select a commodity and run the analysis:** Choose a commodity from the dropdown and click the "Run Analysis" button.
5.  **Explore the results:** Analyze the charts and metrics to understand the risk profile of the selected commodity.

## 5. Interpreting the Results

### Number of Exceptions

The "Number of Exceptions" is a key metric for evaluating the performance of the Value-at-Risk (VaR) model. Here's a breakdown of what it means:

-   **Value-at-Risk (VaR):** The VaR (95%) is an estimate of the maximum potential loss on a given day, with 95% confidence. In other words, we expect the actual loss to be less than the VaR on 95% of the days.

-   **Exception:** An "exception" occurs when the actual loss on a given day is *greater* than the VaR estimate for that day. It means the model underestimated the risk on that day.

-   **Expected Number of Exceptions:** Since the VaR is calculated at a 95% confidence level, we expect to see exceptions on 5% of the days. The "Expected" number is calculated as: `Total number of days * 0.05`.

**A good model should have a number of exceptions that is close to the expected number.** If the actual number of exceptions is much higher than the expected number, it means the model is underestimating the risk. If it's much lower, the model might be overestimating the risk.