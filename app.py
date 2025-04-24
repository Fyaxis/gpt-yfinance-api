from flask import Flask, request, jsonify
from get_stock_data import get_stock_info

app = Flask(__name__)

@app.route('/api/stock', methods=['GET'])
def get_stock():
    symbols = request.args.get('symbols', 'AAPL').split(',')
    report = request.args.get('report', 'summary')  # summary, income, balance, cashflow
    data = get_stock_info(symbols, report)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
