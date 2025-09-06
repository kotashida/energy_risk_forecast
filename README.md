# Energy Risk Forecasting Dashboard

## 1. Project Overview

This project delivers an interactive dashboard for forecasting the volatility of energy commodities (WTI crude oil and Henry Hub natural gas) and quantifying potential market risks. It applies rigorous econometric modeling (ARIMA-GARCH/EGARCH) to generate daily risk metrics, including Value-at-Risk (VaR) and Expected Shortfall (ES), enabling traders, analysts, and risk managers to make more informed decisions.

The dashboard provides a clear and intuitive interface for exploring risk, with a focus on robust statistical analysis and model validation.

## 2. Core Features

-   **Automated Data Ingestion:** Fetches the latest WTI and Henry Hub prices from the FRED API.
-   **Advanced Volatility Modeling:**
    -   Fits ARIMA models to capture underlying trends in the price data.
    -   Offers a choice between GARCH and EGARCH models to forecast future volatility.
    -   Allows for the selection of different distributions (Normal or Student's t) to better model the characteristics of financial returns.
-   **Comprehensive Risk Calculation:** Computes daily VaR and ES based on the selected model and distribution.
-   **Multi-day Forecasting:** Provides multi-day volatility forecasts with an interactive slider to select the forecast horizon.
-   **Rigorous Backtesting:** Validates the accuracy of the VaR models against historical data and provides a clear interpretation of the results.
-   **Interactive Dashboard:** Visualizes prices, conditional volatility, forecasted volatility, and backtesting results.
-   **Downloadable Reports:** Allows users to download the analysis results in a CSV format.

## 3. Methodology

### 3.1. Time Series Analysis

The project begins by transforming the raw price data into logarithmic returns, which are more suitable for statistical modeling. An **ARIMA (Autoregressive Integrated Moving Average)** model is then fitted to the returns to account for any serial correlation. The residuals from the ARIMA model are then used as the input for the volatility modeling stage.

### 3.2. Volatility Modeling

The volatility of financial returns is not constant over time. To capture this, the project employs two advanced econometric models:

-   **GARCH (Generalized Autoregressive Conditional Heteroskedasticity):** This model is used to forecast the conditional variance (volatility) of the returns. It is chosen for its ability to model volatility clustering, a common feature of financial time series where periods of high volatility are followed by more high volatility, and periods of low volatility are followed by more low volatility.
-   **EGARCH (Exponential GARCH):** This is an extension of the GARCH model that also captures the "leverage effect," where negative shocks (e.g., price drops) have a greater impact on volatility than positive shocks of the same magnitude.

The choice between GARCH and EGARCH allows for a more flexible and accurate representation of the underlying volatility dynamics.

### 3.3. Risk Quantification

The project calculates two key risk metrics:

-   **Value-at-Risk (VaR):** This is a statistical measure of the potential loss in value of a portfolio over a defined period for a given confidence interval. For example, a 95% VaR of $1 million means that there is a 5% chance of losing more than $1 million over the next day.
-   **Expected Shortfall (ES):** Also known as Conditional VaR (CVaR), this metric answers the question, "If things do go bad, what is our expected loss?" It is calculated as the average of all losses that are greater than or equal to the VaR. ES is considered a more robust measure of risk than VaR because it provides a better sense of the tail risk.

### 3.4. Model Validation

To ensure the reliability of the risk models, the project includes a **backtesting** module. This involves comparing the predicted VaR with the actual returns over a historical period. The number of "exceptions" (days where the actual loss exceeded the VaR) is counted and compared to the expected number of exceptions based on the chosen confidence level. A model is considered well-calibrated if the number of actual exceptions is close to the number of expected exceptions.

## 4. Key Quantitative Skills

-   **Time Series Analysis:** ARIMA modeling, stationarity testing, and residual analysis.
-   **Econometric Modeling:** GARCH and EGARCH for volatility forecasting.
-   **Probability and Statistics:** Normal and Student's t-distributions, confidence intervals, and hypothesis testing.
-   **Risk Management:** Value-at-Risk (VaR) and Expected Shortfall (ES) calculation and interpretation.
-   **Model Validation:** Historical backtesting of VaR models.

## 5. Tech Stack

-   **Language:** Python
-   **Core Libraries:**
    -   **Data Manipulation:** pandas
    -   **Time Series Modeling:** statsmodels (for ARIMA), arch (for GARCH/EGARCH)
    -   **Dashboard:** Streamlit
    -   **Data Visualization:** Plotly, Altair

## 6. Installation and Usage

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
