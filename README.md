
# TW Stock Bot v13 財報強化版

## 這版新增
- 全台股價格 CSV 批次匯入器
- 啟動時自動掃描價格資料夾 `data/batch_import`
- 寶藏股完整財報資料匯入器
- 啟動時自動掃描財報資料夾 `data/financial_batch`
- 長期寶藏股加入多年度現金流 / 股利 / 自由現金流評分
- 含手續費 / 證交稅 / 滑價的正式回測
- 全部時間統一 Asia/Taipei（UTC+8）
- 禁用逐筆即時資料，改用 stable/delayed snapshot

## 執行
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 主要頁面
- `/` Dashboard
- `/ranking` 短線排行榜
- `/treasure` 長期寶藏股
- `/backtest` 成本/滑價回測摘要
- `/import-tool` 價格 / 財報匯入工具

## 價格 CSV 格式
- date
- open
- high
- low
- close
- volume

## 財報 CSV 格式
- year
- revenue
- gross_margin
- roe
- eps
- operating_cf
- capex
- free_cf
- dividend

## 批次匯入
### 價格資料
1. 把多檔 CSV 丟到 `data/batch_import/`
2. 啟動服務時會自動掃描
3. 或到 `/import-tool` 手動按批次匯入

### 財報資料
1. 把多檔 CSV 丟到 `data/financial_batch/`
2. 啟動服務時會自動掃描
3. 或到 `/import-tool` 手動按批次匯入財報

## 寶藏股評分（長期）
除了 PE / PB / ROE / 毛利率 / 3Y CAGR / 多季趨勢，這版新增：
- 年度營收連升
- 年度 EPS 連升
- 年度毛利率連升
- 年度 ROE 連升
- 自由現金流正值年數
- 營業現金流正值年數
- 連續配息年數
- 平均自由現金流率

## 目前功能
1. 短線 1–10 天排行榜
2. 每檔價格策略：回踩、追價、止損、TP1/TP2/TP3
3. 多策略正式回測
4. 成本/滑價納入
5. 長期低估寶藏股獨立一格
6. 價格與財報批次匯入 / 啟動自動掃描

## 目前仍不足
1. 尚未內建全台股完整真歷史與完整財報資料庫，仍需你自行匯入 CSV
2. 回測未納入漲跌停無法成交、分點、融資券等細節
3. 寶藏股已納入多年度現金流/股利/FCF，但尚未加入完整自由現金流折現估值、庫藏股/資本配置品質


## v14 長線估值模組
- `/treasure`: 長期低估股列表
- `/thesis`: 長期 thesis 報表
- 估值：DCF、EV/EBITDA、安全邊際
- 股利：配息年數、穩定度、覆蓋率

注意：v14 的 DCF 與 EV/EBITDA 仍是研究型模型，不是審計級估值引擎。若你匯入更完整的股本、淨負債與 EBITDA 資料，結果會更準。
