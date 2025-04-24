import requests
import feedparser
import yfinance as yf
from flask import request, jsonify

GNEWS_API_KEY = "3d6996eeeef48bdba216e440cd4b54d8"

def get_news():
    query = request.args.get("q", "")
    from_date = request.args.get("from", "")
    to_date = request.args.get("to", "")
    lang = request.args.get("lang", "en")
    max_results = request.args.get("max", "10")

    result = {}

    # 1. GNews 查询
    gnews = _get_gnews(query, from_date, to_date, lang, max_results)
    result["GNews"] = gnews.get("articles", []) if gnews else []

    # 2. Google News RSS 查询（多语言支持）
    google = _get_google_news(query, lang, max_results)
    result["Google"] = google if google else []

    # 3. Yahoo Finance 查询（适用于英文股票代码）
    if query.isupper() and len(query) <= 6:
        yahoo = _get_yahoo_news(query)
        result["Yahoo"] = yahoo if yahoo else []
    else:
        result["Yahoo"] = []

    return jsonify(result)


# GNews 查询函数
def _get_gnews(query, from_date, to_date, lang, max_results):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "token": GNEWS_API_KEY,
        "lang": lang,
        "max": max_results
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    try:
        res = requests.get(url, params=params)
        return res.json()
    except:
        return {}

# Yahoo Finance 新闻（symbol）
def _get_yahoo_news(symbol):
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        return [
            {
                "title": n.get("title"),
                "url": n.get("link"),
                "publishedAt": n.get("providerPublishTime"),
                "publisher": n.get("publisher")
            } for n in news
        ]
    except:
        return []

# Google News RSS 多语言支持
def _get_google_news(query, lang, max_results):
    lang_map = {
        "zh": "zh-CN", "en": "en-US", "ja": "ja", "ko": "ko",
        "fr": "fr", "de": "de", "es": "es", "ru": "ru",
        "pt": "pt-PT", "ar": "ar", "hi": "hi", "it": "it"
    }
    lang_code = lang_map.get(lang.lower(), "en-US")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl={lang_code}"

    try:
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:int(max_results)]:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "publishedAt": entry.published if "published" in entry else "",
                "source": f"Google News ({lang_code})"
            })
        return articles
    except:
        return []


# 子接口：分别暴露每一源
def get_gnews():
    return jsonify(_get_gnews(
        query=request.args.get("q", ""),
        from_date=request.args.get("from", ""),
        to_date=request.args.get("to", ""),
        lang=request.args.get("lang", "en"),
        max_results=request.args.get("max", "10")
    ))

def get_yahoo():
    return jsonify(_get_yahoo_news(request.args.get("symbol", "AAPL")))

def get_google():
    return jsonify(_get_google_news(
        request.args.get("q", ""),
        request.args.get("lang", "en"),
        request.args.get("max", "10")
    ))
