import numpy as np
from DataHandler import get_data
import Event


class Strategy:
    def __init__(self, long_window, short_window, size, state, price_history):
        self.long_window = long_window
        self.short_window = short_window
        self.size = size
        self.state = state
        self.price_history = price_history
        pass
