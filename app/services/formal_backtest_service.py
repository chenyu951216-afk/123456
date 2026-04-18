from dataclasses import dataclass
import pandas as pd
from app.core.config import V13_TRADING_FEE_RATE, V13_TAX_RATE, V13_SLIPPAGE_BPS

@dataclass
class BtResult:
    strategy: str
    window: int
    trades: int
    winrate: float
    avg_return: float
    max_drawdown: float
    profit_factor: float

def _net_return(entry: float, exit_: float) -> float:
    slip = V13_SLIPPAGE_BPS / 10000.0
    entry_eff = entry * (1 + slip)
    exit_eff = exit_ * (1 - slip)
    gross = (exit_eff / entry_eff) - 1
    costs = (V13_TRADING_FEE_RATE * 2) + V13_TAX_RATE
    return gross - costs

def _max_drawdown_from_slice(df: pd.DataFrame) -> float:
    peak = df["close"].cummax()
    dd = (df["close"] / peak) - 1
    return float(dd.min() * 100)

def run_strategy(df: pd.DataFrame, strategy: str, window: int = 5) -> BtResult:
    closes = pd.to_numeric(df["close"], errors="coerce")
    highs = pd.to_numeric(df["high"], errors="coerce")
    lows = pd.to_numeric(df["low"], errors="coerce")
    ma20 = closes.rolling(20).mean()
    rets=[]
    dds=[]
    for i in range(25, len(df)-window):
        cond=False
        if strategy == "breakout":
            cond = closes.iloc[i] > highs.iloc[i-20:i].max()
        elif strategy == "pullback":
            cond = closes.iloc[i] > ma20.iloc[i] and lows.iloc[i] <= ma20.iloc[i] * 1.01
        elif strategy == "trend_follow":
            cond = closes.iloc[i] > ma20.iloc[i] and ma20.iloc[i] > ma20.iloc[i-5]
        if cond:
            entry = closes.iloc[i]
            exit_ = closes.iloc[i+window]
            r = _net_return(entry, exit_)
            rets.append(r)
            dds.append(_max_drawdown_from_slice(df.iloc[i:i+window+1]))
    trades = len(rets)
    if not trades:
        return BtResult(strategy, window, 0, 0.0, 0.0, 0.0, 0.0)
    wins = [r for r in rets if r > 0]
    losses = [-r for r in rets if r <= 0]
    pf = (sum(wins) / sum(losses)) if losses and sum(losses)>0 else (999 if wins else 0)
    return BtResult(
        strategy=strategy,
        window=window,
        trades=trades,
        winrate=round(len(wins) / trades * 100, 2),
        avg_return=round(sum(rets) / trades * 100, 2),
        max_drawdown=round(min(dds), 2),
        profit_factor=round(pf, 2) if pf != 999 else 999.0
    )

def multi_strategy_backtest(df: pd.DataFrame):
    results=[]
    for strategy in ["breakout","pullback","trend_follow"]:
        for window in [3,5,10]:
            results.append(run_strategy(df, strategy, window))
    best = sorted(results, key=lambda x: (x.winrate, x.avg_return, x.profit_factor), reverse=True)[0]
    return {
        "best_strategy": best.strategy,
        "best_window": best.window,
        "formal_winrate": best.winrate,
        "avg_return": best.avg_return,
        "max_drawdown": best.max_drawdown,
        "profit_factor": best.profit_factor,
        "trades": best.trades,
        "all_results": results
    }
