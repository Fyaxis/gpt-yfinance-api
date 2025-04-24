from flask import Flask
from get_stock_data import get_stock
from news_api import get_news, get_gnews, get_google, get_yahoo

app = Flask(__name__)
app.route("/api/stock", methods=["GET"])(get_stock)
app.route("/api/news", methods=["GET"])(get_news)
app.route("/api/news/gnews", methods=["GET"])(get_gnews)
app.route("/api/news/google", methods=["GET"])(get_google)
app.route("/api/news/yahoo", methods=["GET"])(get_yahoo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
