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
                if df.empty:
                    results[symbol] = {"error": "No financial data available"}
                else:
                    df = df.fillna(None)
                    results[symbol] = {str(k): v for k, v in df.to_dict().items()}
            elif report == "balance":
                df = ticker.balance_sheet
                if df.empty:
                    results[symbol] = {"error": "No balance sheet data available"}
                else:
                    df = df.fillna(None)
                    results[symbol] = {str(k): v for k, v in df.to_dict().items()}
            elif report == "cashflow":
                df = ticker.cashflow
                if df.empty:
                    results[symbol] = {"error": "No cashflow data available"}
                else:
                    df = df.fillna(None)
                    results[symbol] = {str(k): v for k, v in df.to_dict().items()}
            else:
                results[symbol] = {"error": "Invalid report type"}
        except Exception as e:
            results[symbol] = {"error": str(e)}

    return jsonify(results)
