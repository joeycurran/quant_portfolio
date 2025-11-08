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
        self.direction = direction


class OrderEvent(Event):
    def __init__(self, ticker, date, quantity, direction):
        self.type = "ORDER"
        self.ticker = ticker
        self.date = date
        self.quantity = quantity
        self.direction = direction


class FillEvent(Event):
    def __init__(self, ticker, date, quantity, direction, fill_price, commission):
        self.type = "FILL"
        self.ticker = ticker
        self.date = date
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission
