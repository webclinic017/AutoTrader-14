from sma_agent import SMAAgent
from validation_utils import run_backtest

agent = SMAAgent()

backtest_settings = {
    "history": 50,                      # History available to the agent
    "initial_capital": 10000.0,         # Initial capital available
    "comission": 0.0,                   # Comission
    "verbose": False                    # Verbosity (prints)
}

data_settings = {
    "source": 'oanda',
    "data_kwargs": {
        "instrument": 'SPX500_USD',
        "start": "2021-04-20 10:00:00",
        "end": "2021-05-20 11:00:00",
        "granularity": "M5",
        "price": "M"
    }
}

run_backtest(agent, data_settings, backtest_settings)
