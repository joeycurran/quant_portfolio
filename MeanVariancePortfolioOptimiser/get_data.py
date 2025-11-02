import yfinance as yf


def get_data(tickers, start_date, end_date):
    try:
        data = yf.download(tickers, start=start_date, end=end_date)
        return data["Close"]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
