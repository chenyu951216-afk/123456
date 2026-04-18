
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import dashboard, ranking, treasure, import_tool, backtest, thesis
from app.core.config import V13_AUTO_SCAN_IMPORT_DIR, V13_AUTO_SCAN_FINANCIAL_DIR
from app.services.history_import_service import auto_scan_default_import_folder
from app.services.financial_import_service import auto_scan_default_financial_folder

app = FastAPI(title="TW Stock Bot v13 財報強化")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard.router)
app.include_router(ranking.router)
app.include_router(treasure.router)
app.include_router(import_tool.router)
app.include_router(backtest.router)
app.include_router(thesis.router)

@app.on_event("startup")
def startup_scan_import_folder():
    if V13_AUTO_SCAN_IMPORT_DIR:
        try:
            auto_scan_default_import_folder()
        except Exception:
            pass
    if V13_AUTO_SCAN_FINANCIAL_DIR:
        try:
            auto_scan_default_financial_folder()
        except Exception:
            pass
