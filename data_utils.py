#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data Utility Functions.

Todo:
    * ...
"""

# Built-in modules

# Third-party modules
import tpqoa

# Local modules

def get_historical_data(source: str = 'oanda', data_kwargs: dict = {}):

    # Define API based on selected source
    if source.lower() == 'oanda':

        # Define default data kwargs if None specified
        data_kwargs = data_kwargs or {
            "instrument": 'SPX500_USD',
            "start": "2021-04-22 10:00:00",
            "end": "2021-04-23 11:00:00",
            "granularity": "M1",
            "price": "M"
        }

        data = get_oanda_data(**data_kwargs)

    # TODO: Add Yahoo and other data sources.

    return data

def get_oanda_data(instrument: str = 'SPX500_USD',
                   start: str = "2021-04-22 10:00:00",
                   end: str = "2021-04-23 11:00:00",
                   granularity: str = "M1",
                   price: str = "M",
                   config: str = "oanda.cfg"):
    """Gets data using the OANDA API.

    Args:
        instrument (str, optional): Quantity of interest to retrieve. Defaults to "EUR_USD".
        start (str, optional): Start date. Defaults to "2020-08-10".
        end (str, optional): End date. Defaults to "2020-08-12".
        granularity (str, optional): Time series granularity. Defaults to "M1".
        price (str, optional): Price. Defaults to "M".

    Returns:
        _type_: _description_
    """

    api = tpqoa.tpqoa(config)
    data = api.get_history(instrument, start, end, granularity, price)
    return data
