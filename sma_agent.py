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


class SMAAgent(TradingAgent):
    """Simple Moving Average Agent Class.

    Defines generation infrastructures and provides related information.
    """

    def __repr__(self):
        return 'SMA Agent'

    def apply_policy(self, price):

        # Initialize order variable properly, to track if we opened our position.
        if 'position' not in self.__dict__.keys():
            self.position = False
        if 'prev_fast_ma' not in self.__dict__.keys():
            self.prev_fast_ma = 0
        if 'prev_slow_ma' not in self.__dict__.keys():
            self.prev_slow_ma = 0

        # Shortcut for the settings
        fast_len = self.settings['fast_len']
        slow_len = self.settings['slow_len']

        # Calculate both means
        fast_ma = price.values[-fast_len:].mean()
        slow_ma = price.values[-slow_len:].mean()

        # Look for a crossover event to buy if not in position
        if not self.position and fast_ma > slow_ma and self.prev_fast_ma < self.prev_slow_ma:
            action = 1
            self.position = True

            #print("Buying !")
            #print()

        # Look for a crossover event to sell if in position
        elif self.position and fast_ma < slow_ma and self.prev_fast_ma > self.prev_slow_ma:
            action = -1
            self.position = False

            #print("Selling !")
            #print()

        # Else, do nothing
        else:
            action = 0

        # Update previous moving average variables for next cycle
        self.prev_fast_ma = fast_ma
        self.prev_slow_ma = slow_ma

        return action

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
