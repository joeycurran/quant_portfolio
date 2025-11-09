import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA", "NVDA"]
data = yf.download(tickers, start="2020-01-01", end="2025-01-01")["Close"]

data.to_csv("tech_prices.csv")
