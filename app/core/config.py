
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

TZ_NAME = os.getenv("TZ_NAME", "Asia/Taipei")
TZ = ZoneInfo(TZ_NAME)

def now_tw():
    return datetime.now(TZ)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
OPENAI_MONTHLY_BUDGET_TWD = float(os.getenv("OPENAI_MONTHLY_BUDGET_TWD", "500"))
DATA_MODE = os.getenv("DATA_MODE", "stable")
USE_SAMPLE_DATA = os.getenv("USE_SAMPLE_DATA", "true").lower() == "true"
FORCE_TWSE_API = os.getenv("FORCE_TWSE_API", "false").lower() == "true"

V13_ENABLE_IMPORT_TOOL = os.getenv("V13_ENABLE_IMPORT_TOOL", "true").lower() == "true"
V13_ENABLE_COST_BACKTEST = os.getenv("V13_ENABLE_COST_BACKTEST", "true").lower() == "true"
V13_ENABLE_TREASURE_SCREEN = os.getenv("V13_ENABLE_TREASURE_SCREEN", "true").lower() == "true"

V13_TRADING_FEE_RATE = float(os.getenv("V13_TRADING_FEE_RATE", "0.001425"))
V13_TAX_RATE = float(os.getenv("V13_TAX_RATE", "0.003"))
V13_SLIPPAGE_BPS = float(os.getenv("V13_SLIPPAGE_BPS", "8"))

TREASURE_MAX_PE = float(os.getenv("TREASURE_MAX_PE", "14"))
TREASURE_MAX_PB = float(os.getenv("TREASURE_MAX_PB", "1.6"))
TREASURE_MIN_ROE = float(os.getenv("TREASURE_MIN_ROE", "10"))
TREASURE_MIN_GROSS_MARGIN = float(os.getenv("TREASURE_MIN_GROSS_MARGIN", "18"))
TREASURE_MIN_3Y_REVENUE_CAGR = float(os.getenv("TREASURE_MIN_3Y_REVENUE_CAGR", "5"))
TREASURE_MIN_REV_Q_UP = int(os.getenv("TREASURE_MIN_REV_Q_UP", "3"))
TREASURE_MIN_GM_Q_UP = int(os.getenv("TREASURE_MIN_GM_Q_UP", "2"))
TREASURE_MIN_ROE_Q_UP = int(os.getenv("TREASURE_MIN_ROE_Q_UP", "2"))

V13_BATCH_IMPORT_DIR = os.getenv("V13_BATCH_IMPORT_DIR", "data/batch_import")
V13_IMPORTED_DIR = os.getenv("V13_IMPORTED_DIR", "data/imported")
V13_AUTO_SCAN_IMPORT_DIR = os.getenv("V13_AUTO_SCAN_IMPORT_DIR", "true").lower() == "true"
V13_AUTO_SCAN_EXTENSIONS = [x.strip() for x in os.getenv("V13_AUTO_SCAN_EXTENSIONS", ".csv").split(",") if x.strip()]

V13_FINANCIAL_IMPORT_DIR = os.getenv("V13_FINANCIAL_IMPORT_DIR", "data/financial_batch")
V13_FINANCIAL_STORE_DIR = os.getenv("V13_FINANCIAL_STORE_DIR", "data/financials")
V13_AUTO_SCAN_FINANCIAL_DIR = os.getenv("V13_AUTO_SCAN_FINANCIAL_DIR", "true").lower() == "true"
V13_FINANCIAL_EXTENSIONS = [x.strip() for x in os.getenv("V13_FINANCIAL_EXTENSIONS", ".csv").split(",") if x.strip()]

TREASURE_MIN_FCF_MARGIN = float(os.getenv("TREASURE_MIN_FCF_MARGIN", "3"))
TREASURE_MIN_DIVIDEND_YEARS = int(os.getenv("TREASURE_MIN_DIVIDEND_YEARS", "3"))
TREASURE_MIN_OCF_STABLE_YEARS = int(os.getenv("TREASURE_MIN_OCF_STABLE_YEARS", "3"))
TREASURE_MIN_FCF_POSITIVE_YEARS = int(os.getenv("TREASURE_MIN_FCF_POSITIVE_YEARS", "2"))

V14_ENABLE_VALUATION = os.getenv("V14_ENABLE_VALUATION", "true").lower() == "true"
DCF_DISCOUNT_RATE = float(os.getenv("DCF_DISCOUNT_RATE", "0.10"))
DCF_GROWTH_RATE = float(os.getenv("DCF_GROWTH_RATE", "0.025"))
TREASURE_MIN_MARGIN_OF_SAFETY = float(os.getenv("TREASURE_MIN_MARGIN_OF_SAFETY", "15"))
DIVIDEND_STABILITY_WEIGHT = float(os.getenv("DIVIDEND_STABILITY_WEIGHT", "1.0"))
