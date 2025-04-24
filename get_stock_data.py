import yfinance as yf
from flask import request, jsonify

def get_stock():
    symbols = request.args.get('symbols', 'AAPL').split(',')
    report = request.args.get('report', 'summary')
    results = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
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
            results[symbol] = ticker.financials.to_dict()
        elif report == "balance":
            results[symbol] = ticker.balance_sheet.to_dict()
        elif report == "cashflow":
            results[symbol] = ticker.cashflow.to_dict()
        else:
            results[symbol] = {"error": "Invalid report type"}
    return jsonify(results)
