# utils/helpers.py

import numpy as np

def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def calculate_max_drawdown(equity_curve: np.ndarray) -> float:
    cumulative_max = np.maximum.accumulate(equity_curve)
    drawdowns = (cumulative_max - equity_curve) / cumulative_max
    return np.max(drawdowns)
