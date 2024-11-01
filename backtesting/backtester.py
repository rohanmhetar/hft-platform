import backtrader as bt
import pandas as pd
from strategy import MovingAverageCrossStrategy
from utils.logger import get_logger

logger = get_logger(__name__)

class Backtester:
    def __init__(self, data: pd.DataFrame, cash: float = 100000.0, commission: float = 0.001):
        self.data = data
        self.cash = cash
        self.commission = commission
        self.cerebro = bt.Cerebro()
        self.logger = logger

    def setup(self, strategy_params: dict = None):
        if strategy_params is None:
            strategy_params = {}

        self.cerebro.addstrategy(MovingAverageCrossStrategy, **strategy_params)

        data_feed = bt.feeds.PandasData(
            dataname=self.data,
            fromdate=self.data.index.min(),
            todate=self.data.index.max()
        )
        self.cerebro.adddata(data_feed)
        self.cerebro.broker.set_cash(self.cash)
        self.cerebro.broker.setcommission(commission=self.commission)
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=10)
        self.cerebro.addobserver(bt.observers.Broker)

    def run(self):
        self.logger.info("Starting backtest...")
        results = self.cerebro.run()
        final_value = self.cerebro.broker.getvalue()
        self.logger.info(f"Final Portfolio Value: {final_value}")
        self.cerebro.plot()
        return results

    def get_final_value(self) -> float:
        return self.cerebro.broker.getvalue()
