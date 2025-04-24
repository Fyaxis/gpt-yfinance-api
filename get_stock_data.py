import yfinance as yf
from flask import request, jsonify

def get_stock():
    symbols = request.args.get('symbols', 'AAPL').split(',')
    report = request.args.get('report', 'summary')
    results = {}

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        try:
            if report == "summary":
                info = ticker.info
                results[symbol] = {
                    "name": info.get("shortName"),
                    "price": info.get("currentPrice"),
                    "peRatio": info.get("trailingPE"),
                    "marketCap": info.get("marketCap"),
                    "sector": info.get("sector")
                }

            elif report == "income":
                df = ticker.financials
                results[symbol] = _safe_dict(df)

            elif report == "balance":
                df = ticker.balance_sheet
                results[symbol] = _safe_dict(df)

            elif report == "cashflow":
                df = ticker.cashflow
                results[symbol] = _safe_dict(df)

            elif report == "all":
                results[symbol] = {
                    "income": _safe_dict(ticker.financials),
                    "balance": _safe_dict(ticker.balance_sheet),
                    "cashflow": _safe_dict(ticker.cashflow)
                }

            else:
                results[symbol] = {
                    "income": _safe_dict(ticker.financials),
                    "balance": _safe_dict(ticker.balance_sheet),
                    "cashflow": _safe_dict(ticker.cashflow)
                }

        except Exception as e:
            results[symbol] = {"error": str(e)}

    return jsonify(results)


# 通用函数：将 DataFrame 转为 JSON 合法结构
def _safe_dict(df):
    if df.empty:
        return {"error": "No financial data available"}
    df = df.fillna(0)
    dict_data = df.to_dict()
    safe_result = {}
    for col_key, subdict in dict_data.items():
        col_str = str(col_key)  # 转换 Timestamp
        safe_result[col_str] = {}
        for row_key, value in subdict.items():
            if isinstance(value, (int, float)):
                safe_result[col_str][str(row_key)] = float(value)
            else:
                safe_result[col_str][str(row_key)] = str(value)
    return safe_result
