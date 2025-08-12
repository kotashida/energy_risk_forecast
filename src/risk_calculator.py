import numpy as np
from scipy.stats import norm, t

def calculate_var(forecasted_volatility, nu=None, confidence_level=0.95):
    """Calculates the Value-at-Risk (VaR).

    Args:
        forecasted_volatility (float): The forecasted volatility.
        nu (float): The degrees of freedom for the t-distribution.
        confidence_level (float): The confidence level for the VaR calculation.

    Returns:
        float: The calculated VaR.
    """
    if nu:
        z_score = t.ppf(confidence_level, nu)
    else:
        z_score = norm.ppf(confidence_level)
    var = z_score * np.sqrt(forecasted_volatility)
    return var

def calculate_es(forecasted_volatility, nu=None, confidence_level=0.95):
    """Calculates the Expected Shortfall (ES).

    Args:
        forecasted_volatility (float): The forecasted volatility.
        nu (float): The degrees of freedom for the t-distribution.
        confidence_level (float): The confidence level for the ES calculation.

    Returns:
        float: The calculated ES.
    """
    if nu:
        z_score = t.ppf(confidence_level, nu)
        es = -t.pdf(z_score, nu) / (1 - confidence_level) * (nu + z_score**2) / (nu - 1) * np.sqrt(forecasted_volatility)
    else:
        z_score = norm.ppf(confidence_level)
        es = (1 / (1 - confidence_level)) * norm.pdf(z_score) * np.sqrt(forecasted_volatility)
    return es
