import queue


class Event:
    pass


class MarketEvent(Event):
    def __init__(self, ticker, date, close_price):
        self.type = "MARKET"
        self.ticker = ticker
        self.date = date
        self.close_price = close_price


class SignalEvent(Event):
    def __init__(self, ticker, date, direction):
        self.type = "SIGNAL"
        self.ticker = ticker
        self.date = date
        self.direction = direction  # 'BUY', 'SELL', or 'EXIT'


class OrderEvent(Event):
    """
    Handles an order to be sent to the ExecutionHandler.
    """

    def __init__(self, ticker, date, quantity, direction):
        self.type = "ORDER"
        self.ticker = ticker
        self.date = date
        self.quantity = quantity  # e.g., 100
        self.direction = direction  # 'BUY' or 'SELL'


class FillEvent(Event):
    """
    Encapsulates a filled order, as returned from a broker.
    This is what the Portfolio uses to update its state.
    """

    def __init__(self, ticker, date, quantity, direction, fill_price, commission):
        self.type = "FILL"
        self.ticker = ticker
        self.date = date
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission
