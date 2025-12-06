import requests

def get_iran_prices():
    url = "https://api.tgju.org/v1/market/summary"
    r = requests.get(url).json()
    data = r["data"]
    return {
        "sekke_emami": int(data["sekee"]["p"]),
        "nim": int(data["nim"]["p"]),
        "rob": int(data["rob"]["p"]),
        "geram18": int(data["geram18"]["p"]),
        "dollar": int(data["dollar_rl"]["p"])
    }

def get_global_gold():
    url = "https://api.metals.live/v1/spot"
    r = requests.get(url).json()
    return float(r[0]["gold"])