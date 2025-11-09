# Project 3: Financial Time Series Toolkit
# Goal: Create reusable functions to compute performance metrics.
# What to implement:
# 	Daily returns, cumulative returns, log returns.
# 	Moving averages, exponential smoothing.
# 	Sharpe ratio, Sortino ratio, maximum drawdown.
# Stretch: Automatically handle missing dates (reindexing + interpolation).
# Libraries: pandas, numpy

import numpy as np
import pandas as pd
import yfinance as yf


def daily_returns(data):
    adj_close = data["Adj Close"] if "Adj Close" in data.columns else data["Close"]

    simple_returns = adj_close.pct_change().dropna()  # total percent chagne
    log_returns = np.log(
        adj_close / adj_close.shift(1)
    ).dropna()  # continuous compounding
    return pd.DataFrame({"simple_return": simple_returns, "log_return": log_returns})


def cumulative_returns(data):
    p_0 = data["Open"].iloc[0]
    p_end = data["Close"].iloc[-1]
    cr = (p_end - p_0) / p_0
    return cr


def cumulative_returns_series(data):
    daily = data["Adj Close"].pct_change().dropna()
    return (1 + daily).cumprod() - 1


def moving_avgs(data, window=20):
    # take avgs over short windows to smooth long term noise
    close = data["Close"]
    sma = close.rolling(window=window).mean()
    ema = close.ewm(span=window, adjust=False).mean()
    return sma, ema


def ratios(data, risk_free_rate=0.2):
    data = data.dropna()
    daily_mean = data.mean()
    daily_std = data.std()
    sharpe = (daily_mean - risk_free_rate / 252) / daily_std * np.sqrt(252)
    # Sharpe measures risk-adjusted return how much excess return you earn per unit of total risk.
    # The MDD formula compares the peak value of an investment to its trough value,
    # expressed as a percentage loss from the peak.
    downside_std = data[data < 0].std()
    # Sortino tells you how much excess return you earn per unit of bad volatility.
    # Assymetric risk, i.e. doesnt care about volatility in positive returns
    sortino = (daily_mean - risk_free_rate / 252) / downside_std * np.sqrt(252)

    cumulative = (1 + data).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    # tells you your worst percentage loss from a previous high.

    return sharpe, sortino, max_drawdown


def get_data(tickers, start_date, end_date):
    try:
        data = yf.download(tickers, start=start_date, end=end_date)
        if isinstance(data.columns, pd.MultiIndex):
            # Flatten MultiIndex columns if multiple tickers
            # i.e. splits multiple tickers into single level columns
            # each then has values
            data.columns = data.columns.get_level_values(0)

        # Reindex to include all business days
        full_index = pd.date_range(data.index.min(), data.index.max(), freq="B")
        data = data.reindex(full_index)

        # Interpolate missing values for prices
        price_cols = ["Open", "High", "Low", "Close", "Adj Close"]
        for col in price_cols:
            if col in data.columns:
                data[col] = data[col].interpolate(
                    method="time"
                )  # pandas uses the actual timestamps in your DateTimeIndex to compute the interpolation weights.
                # it adds data for the reindexed dates using linear interpolation based on time, i.e. half way between two known data points
        # Forward fill Volume
        # interpolates using previous value for missing volume data, can be bad for certain metrics, weekend volume and holidays always 0
        if "Volume" in data.columns:
            data["Volume"] = data["Volume"].fillna(method="ffill")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def main():
    data = get_data("AAPL", "2020-07-24", "2023-07-28")

    rets = daily_returns(data)
    print("Daily returns (simple):")
    print(rets["simple_return"].head())

    print("\nCumulative return:")
    print(cumulative_returns(data))

    sma, ema = moving_avgs(data)
    print("\n20-day SMA (last 5):")
    print(sma.tail())
    print("\n20-day EMA (last 5):")
    print(ema.tail())

    sharpe, sortino, max_dd = ratios(rets["simple_return"])
    print("\nSharpe Ratio:", sharpe)
    print("Sortino Ratio:", sortino)
    print("Max Drawdown:", max_dd)


if __name__ == "__main__":
    main()
