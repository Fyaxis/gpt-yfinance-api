import requests
from flask import request, jsonify

GNEWS_API_KEY = "3d6996eeeef48bdba216e440cd4b54d8"
GNEWS_ENDPOINT = "https://gnews.io/api/v4/search"

def get_news():
    query = request.args.get("q", "finance")
    from_date = request.args.get("from", "")
    to_date = request.args.get("to", "")
    lang = request.args.get("lang", "en")
    max_results = request.args.get("max", "10")

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

    response = requests.get(GNEWS_ENDPOINT, params=params)
    return jsonify(response.json())
