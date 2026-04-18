from pathlib import Path
import pandas as pd
from app.services.sample_data_service import sample_history

BASE = Path("data/history")
IMPORTED = Path("data/imported")

def list_available_symbols():
    symbols = set()
    for root in [BASE, IMPORTED]:
        if root.exists():
            for p in root.glob("*.csv"):
                symbols.add(p.stem)
    return sorted(symbols)

def load_history(stock_id: str, min_rows: int = 60) -> pd.DataFrame:
    for folder in [IMPORTED, BASE]:
        path = folder / f"{stock_id}.csv"
        if path.exists():
            df = pd.read_csv(path)
            cols = {c.lower(): c for c in df.columns}
            mapping = {}
            for k in ["date","open","high","low","close","volume"]:
                if k in cols: mapping[cols[k]] = k
            df = df.rename(columns=mapping)
            needed = ["date","open","high","low","close","volume"]
            if all(c in df.columns for c in needed):
                return df[needed].tail(max(min_rows, len(df)))
    return sample_history(stock_id, max(min_rows, 220))
