#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Trading Agent Base Class

Validation and backtrading functionalities.

Todo:
    * ...
"""

# Built-in modules

# Third-party modules
import backtrader as bt
import pandas as pd

# Local modules
from data_utils import get_historical_data

def run_backtest(agent, data, settings: dict):
    """Runs a backtesting procedure to assert performance on historical data.
    """

    # Prepare and feed data in required format
    data_is_df = isinstance(data, pd.DataFrame)
    data = data if data_is_df else get_historical_data(**data)
    data = data.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "volume": "Volume",
        "complete": "OpenInterest"})
    #print(data.iloc[0:10])
    bt_data = bt.feeds.PandasData(dataname=data)

    StrategyWrapper = _define_strategy_wrapper(agent, settings, data)

    # Backtest class instance
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(settings['initial_capital'])
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(settings['comission'])
    cerebro.addstrategy(StrategyWrapper)
    cerebro.adddata(bt_data)

    # Backtest execution and results
    #print()
    #print("*----------------------*")
    print("*- BACKTEST EXECUTION -*")
    #print("*----------------------*")
    starting_capital = cerebro.broker.getvalue()
    cerebro.run()
    end_capital = cerebro.broker.getvalue()
    print()
    print("*--------------------*")
    print("*- BACKTEST RESULTS -*")
    print("*--------------------*")
    print(f'Starting Portfolio Value: {starting_capital}')
    print(f'Final Portfolio Value:    {end_capital}')
    print(f"Gain (%): {(end_capital-starting_capital)*100/starting_capital}")

    cerebro.plot()

def _define_strategy_wrapper(agent, settings, data):

    class StrategyWrapper(bt.Strategy):

        def __init__(self):

            # Define data streams to follow
            self.data_close = self.datas[0].close
            self.data_open = self.datas[0].open
            self.data_high = self.datas[0].high
            self.data_low = self.datas[0].low
            self.data_volume = self.datas[0].volume

            # Order variable will contain ongoing order details/status
            self.order = None

            self.bar_executed = None

        """
        def notify_trade(self, order):
            t = self._get_current_index()

            if order.status in [order.Submitted, order.Accepted]:
                # An active Buy/Sell order has been submitted/accepted - Nothing to do
                return

            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    print(
                        f'Buy executed at {t} for {order.executed.price}$')
                elif order.issell():
                    print(
                        f'Sell executed at {t} for {order.executed.price}$')
                self.bar_executed = len(self)

            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                print('Order Canceled/Margin/Rejected')

            # Reset orders
            self.order = None
        """

        def next(self):
            t = self._get_current_index()

            if settings['verbose']:
                print(f"{t} - Epoch: {len(self)}, Bar Executed: {self.bar_executed}")

            # Check for open orders
            if self.order:
                return

            # Check if we are in the market
            #if not self.position and len(self) >= settings['history']:
            if len(self) >= settings['history']:
                history = settings['history']
                close_data = list(self.data_close.get(size=history))
                open_data = list(self.data_open.get(size=history))
                high_data = list(self.data_high.get(size=history))
                low_data = list(self.data_low.get(size=history))
                volume_data = list(self.data_volume.get(size=history))
                idx = data.index.values[len(self) - history:len(self)]
                df = pd.DataFrame(
                    {"Open": open_data,
                     "Close": close_data,
                     "High": high_data,
                     "Low": low_data,
                     "Volume": volume_data}, index=idx)

                action = agent.apply_policy(df)

                if action == 1:
                    self.buy()
                elif action == 0:
                    pass
                elif action == -1:
                    self.sell()
                #self.order = self.close()

                else:
                    print('Incorrect agent apply policy return. Use 1,0,-1.')

        def _get_current_index(self):
            return self.datas[0].datetime.datetime()

    return StrategyWrapper
