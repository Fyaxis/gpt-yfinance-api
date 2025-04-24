from flask import Flask
from get_stock_data import get_stock
from news_api import get_news

app = Flask(__name__)
app.route("/api/stock", methods=["GET"])(get_stock)
app.route("/api/news", methods=["GET"])(get_news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
