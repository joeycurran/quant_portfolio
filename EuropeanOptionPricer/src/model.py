from scipy.stats import norm
import numpy as np
from numpy import log, sqrt, exp


class EuropeanOptionPricerModel:
    def __init__(
        self, spot_price, strike_price, time_to_maturity, risk_free_rate, volatility
    ):
        """Initializes the pricing model with option parameters."""
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

    def _calculate_d1_d2(self):
        """Private helper method to calculate d1 and d2."""
        S = self.spot_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.volatility

        # Handle T=0 edge case to avoid division by zero
        if T == 0:
            return np.inf if S > K else -np.inf, np.inf if S > K else -np.inf

        d1 = (log(S / K) + (r + (sigma**2 / 2)) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        return d1, d2

    def bsm_call_price(self):
        """Calculates the BSM price for a European call option."""
        S = self.spot_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate

        if T == 0:
            return np.maximum(S - K, 0)

        d1, d2 = self._calculate_d1_d2()
        call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        return call_price

    def bsm_put_price(self):
        """Calculates the BSM price for a European put option."""
        S = self.spot_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate

        if T == 0:
            return np.maximum(K - S, 0)

        d1, d2 = self._calculate_d1_d2()
        put_price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price

    def _simulate_terminal_prices(self, num_simulations):
        """Private helper to simulate all terminal prices."""
        if self.time_to_maturity == 0:
            # If T=0, all "simulated" prices are just the current price
            return np.full(num_simulations, self.spot_price)

        S0 = self.spot_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.volatility

        Z = np.random.normal(size=num_simulations)
        S_T = S0 * exp((r - 0.5 * sigma**2) * T + sigma * sqrt(T) * Z)
        return S_T

    def monte_carlo_call_price(self, num_simulations):
        """Calculates the MC price for a European call option."""
        S_T = self._simulate_terminal_prices(num_simulations)

        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate

        payoffs = np.maximum(S_T - K, 0)
        price = exp(-r * T) * np.mean(payoffs)
        return price

    def monte_carlo_put_price(self, num_simulations):
        """Calculates the MC price for a European put option."""
        S_T = self._simulate_terminal_prices(num_simulations)

        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate

        payoffs = np.maximum(K - S_T, 0)
        price = exp(-r * T) * np.mean(payoffs)
        return price
