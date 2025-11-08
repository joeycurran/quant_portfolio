import yfinance as yf
import pandas as pd
import Event
import queue


class DataHandler:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.all_data = self.get_data(tickers, start_date, end_date)
        self.data_iterator = self.all_data.itertuples()

    def get_data(self, tickers, start_date, end_date):
        try:
            data = yf.download(tickers, start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def get_next_bar(self):
        try:
            row = next(self.data_iterator)
            ticker = self.tickers[0]
            market_event = Event.MarketEvent(ticker, row.Index, row.Close)
            self.queue.put(market_event)
            return
        except StopIteration:
            return None
