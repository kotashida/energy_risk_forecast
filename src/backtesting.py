import pandas as pd
import numpy as np
from scipy.stats import norm, t

def backtest_var(returns, conditional_vol, nu=None, confidence_level=0.95):
    """Performs a historical backtest of the VaR model.

    Args:
        returns (pd.Series): The historical returns of the asset.
        conditional_vol (pd.Series): The conditional volatility from the GARCH model.
        nu (float): The degrees of freedom for the t-distribution.
        confidence_level (float): The confidence level for the VaR calculation.

    Returns:
        tuple: A tuple containing the number of exceptions and the historical VaR series.
    """
    if nu:
        z_score = t.ppf(confidence_level, nu)
    else:
        z_score = norm.ppf(confidence_level)
    historical_var = -z_score * conditional_vol
    exceptions = returns[returns < -historical_var]
    return len(exceptions), -historical_var
