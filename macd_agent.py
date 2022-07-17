#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Moving Average Agent

Todo:
    * ...
"""

# Built-in modules

# Third-party modules

# Local modules
from trading_agent import TradingAgent


class  MacDAgent(TradingAgent):
    """Simple Moving Average Agent Class.

    Defines generation infrastructures and provides related information.
    """

    def __init__(self):
        self.position_open = False 
        self.price_bought = 0

    def __repr__(self):
        return 'SMA Agent'

    def apply_policy(self, price):

        price = price.values

        action = 0

        short_ma_now = price[-12].mean()
        long_ma_now = price[-28].mean()

        short_ma_past = price[-13:-1].mean()
        long_ma_past = price[-29:-1].mean()

        # Buying
        if self.position_open == False and long_ma_past > short_ma_past and long_ma_now < short_ma_past:
            action = 1
            self.price_bought = price[-1]
            self.position_open = True

        # Selling
        if self.position_open == True:
            if price[-1] >= 1.001*self.price_bought or price[-1] <= 0.9995*self.price_bought:
                action = -1
                self.position_open = False

        return action


    """
    #RSI
    def __init__(self):
        self.position_open = False 
        self.price_bought = 0

    def __repr__(self):
        return 'SMA Agent'

    def apply_policy(self, price):

        price = price.values

        action = 0

        average_gain_14 = price[-15:-1].mean

        rsi_prime = 100 - (100/(1+(average_gain_14/average_loss_l4)))

    def avg_gain(self,price):

        average_gain_14 = price[-15:-1].mean
    """


    @staticmethod
    def get_default_settings() -> dict:
        """Returns the class' default settings dictionary.

        Returns:
            dict: Default settings dictionary.
        """

        def_config = {
            "fast_len": 20,
            "slow_len": 50
        }

        return def_config

