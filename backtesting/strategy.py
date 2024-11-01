import backtrader as bt
import numpy as np

class MovingAverageCrossStrategy(bt.Strategy):
    params = (
        ('fast_period', 50),
        ('slow_period', 200),
        ('order_percentage', 0.95),
        ('ticker', 'AAPL')
    )

    def __init__(self):
        self.ticker = self.params.ticker
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_period, plotname='50 day moving average'
        )
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_period, plotname='200 day moving average'
        )
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        self.volume = self.datas[0].volume

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.log(f'BUY EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                size = int(self.broker.getcash() * self.params.order_percentage / self.dataclose)
                self.log(f'BUY CREATE, {self.dataclose[0]}, Size: {size}')
                self.order = self.buy(size=size)
        else:
            if self.crossover < 0:
                self.log(f'SELL CREATE, {self.dataclose[0]}')
                self.order = self.sell(size=self.position.size)

    def stop(self):
        self.log(f'Ending Value {self.broker.getvalue()}', dt=self.datas[0].datetime.date(0))
