
from app.services.sample_data_service import (
    stock_master, sample_fundamentals, sample_quarterly_fundamentals,
    sample_financial_histories,
)
from app.services.real_kline_service import load_history
from app.services.technical_service import build_features
from app.services.formal_backtest_service import multi_strategy_backtest
from app.services.treasure_stock_service import score_treasure
from app.services.financial_import_service import load_financial_history


def _short_term_score(tech, bt, fundamentals):
    score = 0
    score += 20 if tech["last_close"] > tech["ma20"] else 0
    score += 15 if tech["ma20"] > tech["ma60"] else 0
    score += min(max(tech["pct_20d"], 0), 20)
    score += min(tech["volume_ratio_20"] * 8, 16)
    score += max(min(bt["formal_winrate"] / 5, 20), 0)
    score += max(min(bt["profit_factor"] * 3, 12), 0)
    score += max(min(fundamentals.get("roe",0)/2, 10), 0)
    score += max(min(fundamentals.get("gross_margin",0)/4, 10), 0)
    return round(score, 2)


def _strategy(stock, tech, bt):
    close = tech["last_close"]
    atr_pct = tech.get("atr_pct", 4) / 100.0
    pullback = round(max(tech["ma20"], close * (1 - atr_pct*0.6)), 2)
    breakout = round(max(close * 1.015, tech["recent_high_20"] * 1.003), 2)
    stop = round(min(tech["recent_low_20"], close * (1 - max(0.04, atr_pct*1.2))), 2)
    risk = max(close - stop, close * 0.03)
    tp1 = round(close + risk * 1.2, 2)
    tp2 = round(close + risk * 2.0, 2)
    tp3 = round(close + risk * 3.0, 2)
    return {
        "pullback_entry": pullback,
        "breakout_entry": breakout,
        "stop_loss": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "holding_days": int(bt["best_window"]),
        "strategy_comment": f"短線以 {bt['best_strategy']} / {bt['best_window']} 天窗較佳。"
    }


def _financial_history_for_symbol(symbol, sample_map):
    imported = load_financial_history(symbol)
    if imported is not None:
        return imported.to_dict(orient='records')
    return sample_map.get(symbol, [])


def build_rankings():
    master = stock_master()
    fundamentals_map = sample_fundamentals()
    quarterly_map = sample_quarterly_fundamentals()
    fin_hist_map = sample_financial_histories()
    ranked=[]
    treasure=[]
    for s in master:
        sid = s["stock_id"]
        df = load_history(sid, 220)
        tech = build_features(df)
        bt = multi_strategy_backtest(df)
        fund = fundamentals_map.get(sid, {})
        quarterly = quarterly_map.get(sid, {})
        fin_hist = _financial_history_for_symbol(sid, fin_hist_map)
        short_score = _short_term_score(tech, bt, fund)
        strategy = _strategy(s, tech, bt)
        tscore = score_treasure(s, fund, tech, bt, quarterly, fin_hist)
        item = {
            **s, **fund, **tech, **bt, **strategy, **tscore,
            "total_score": short_score
        }
        ranked.append(item)
        if tscore["is_treasure_candidate"]:
            treasure.append(item)
    ranked = sorted(ranked, key=lambda x: x["total_score"], reverse=True)
    treasure = sorted(treasure, key=lambda x: (x["treasure_score"], x.get("dcf_margin_of_safety", 0), -x.get("ev_ebitda", 999), x.get("dividend_stability_score", 0), x["financial_trend_score"], x["quarterly_trend_score"]), reverse=True)
    for i, item in enumerate(ranked[:5], start=1):
        item["rank"] = i
    for i, item in enumerate(treasure[:10], start=1):
        item["treasure_rank"] = i
    return {
        "ranking": ranked[:10],
        "top5": ranked[:5],
        "treasure": treasure[:10]
    }
