import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

def fit_arima(data, p=5, d=1, q=0):
    """Fits an ARIMA model to the data.

    Args:
        data (pd.Series): The time series data.
        p (int): The order (number of time lags) of the autoregressive model (AR).
        d (int): The degree of differencing (the number of times the data have had past values subtracted) (I).
        q (int): The order of the moving-average model (MA).

    Returns:
        ARIMAResults: The fitted ARIMA model results.
    """
    model = ARIMA(data, order=(p, d, q))
    model_fit = model.fit()
    return model_fit

def fit_garch(residuals, p=1, q=1, o=1, dist='normal', vol='Garch'):
    """Fits a GARCH model to the residuals.

    Args:
        residuals (pd.Series): The residuals from the ARIMA model.
        p (int): The order of the GARCH lags.
        q (int): The order of the ARCH lags.
        o (int): The order of the asymmetric term (for EGARCH).
        dist (str): The distribution to use for the model.
        vol (str): The volatility model to use.

    Returns:
        GARCHResults: The fitted GARCH model results.
    """
    if vol == 'EGARCH':
        model = arch_model(residuals, vol=vol, p=p, o=o, q=q, dist=dist)
    else:
        model = arch_model(residuals, vol=vol, p=p, q=q, dist=dist)
    model_fit = model.fit(disp='off')
    return model_fit

def forecast_volatility(garch_model, horizon=1):
    """Forecasts the volatility using the fitted GARCH model.

    Args:
        garch_model (GARCHResults): The fitted GARCH model.
        horizon (int): The forecast horizon.

    Returns:
        pd.DataFrame: The forecasted volatility.
    """
    forecast = garch_model.forecast(horizon=horizon)
    return forecast.variance.iloc[-1, :]
