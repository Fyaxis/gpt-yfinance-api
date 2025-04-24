import yfinance as yf

def get_stock_info(symbols, report_type):
    results = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        if report_type == "summary":
            info = ticker.info
            results[symbol] = {
                "name": info.get("shortName"),
                "price": info.get("currentPrice"),
                "peRatio": info.get("trailingPE"),
                "marketCap": info.get("marketCap"),
                "sector": info.get("sector")
            }
        elif report_type == "income":
            results[symbol] = ticker.financials.to_dict()
        elif report_type == "balance":
            results[symbol] = ticker.balance_sheet.to_dict()
        elif report_type == "cashflow":
            results[symbol] = ticker.cashflow.to_dict()
        else:
            results[symbol] = {"error": "Invalid report type"}
    return results
