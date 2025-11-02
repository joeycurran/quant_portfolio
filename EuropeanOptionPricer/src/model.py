from scipy.stats import norm
import numpy as np
from numpy import log, sqrt, exp


class EuropeanOptionPricerModel:
    def __init__(
        self,
        spot_price,
        strike_price,
        time_to_maturity,
        risk_free_rate,
        volatility,
    ):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

    def bsm_price(self, option_type):
        S = self.spot_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.volatility
        call_price = None
        put_price = None

        if T == 0:
            return np.maximum(S - K, 0)
        d1 = (np.log(S / K) + (r + (sigma**2 / 2)) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type in ("call", "all"):
            call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            return call_price, put_price
        elif option_type in ("put", "all"):
            put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            return call_price, put_price
        else:
            return call_price, put_price

    def monte_carlo_price(self, num_simulations, option_type="call"):
        if self.time_to_maturity == 0:
            return np.maximum(self.spot_price - self.strike_price, 0)

        S0 = self.spot_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.volatility
        call_price = None
        put_price = None

        Z = np.random.normal(size=num_simulations)
        S_T = S0 * exp((r - 0.5 * sigma**2) * T + sigma * sqrt(T) * Z)
        payoffs_call = np.maximum(S_T - K, 0)
        payoffs_put = np.maximum(K - S_T, 0)
        if option_type in ("call", "all"):
            call_price = exp(-r * T) * np.mean(payoffs_call)
            return call_price, None
        elif option_type in ("put", "all"):
            put_price = exp(-r * T) * np.mean(payoffs_put)
            return call_price, put_price
        else:
            return call_price, put_price
