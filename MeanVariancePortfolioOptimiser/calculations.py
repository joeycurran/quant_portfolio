from get_data import get_data
import numpy as np
import scipy.optimize


def calculate_log_returns(price_data):
    return np.log(price_data / price_data.shift(1)).iloc[1:]


def calculate_annualized_mean_returns(log_returns_df):
    return log_returns_df.mean() * 252


def calculate_annualized_covariance(log_returns_df):
    return log_returns_df.cov() * 252


def calculate_portfolio_variance(weights, sigma):
    return weights.T @ sigma @ weights


def calculate_portfolio_return(weights, mu):
    return weights.T @ mu


def calculate_portfolio_volatility(weights, sigma):
    return np.sqrt(calculate_portfolio_variance(weights, sigma))


def optimize_portfolio(sigma):
    # number of assets from the covariance matrix
    num_assets = sigma.shape[0]

    # Define the bounds (Long-Only: 0 <= w_i <= 1)
    bounds = tuple((0, 1) for _ in range(num_assets))

    # Define the constraint  sum(w) = 1

    constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}

    # Set an initial guess with equal eights
    initial_weights = np.ones(num_assets) / num_assets

    result = scipy.optimize.minimize(
        calculate_portfolio_variance,
        initial_weights,
        args=(sigma,),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if result.success:
        # Return the optimal weights
        return result.x
    else:
        # Raise an error if the solver failed
        raise ValueError(f"Optimization failed: {result.message}")
