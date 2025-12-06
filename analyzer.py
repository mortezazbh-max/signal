def analyze(prices, global_gold):
    s = prices["sekke_emami"]
    g18 = prices["geram18"]
    usd = prices["dollar"]

    fair_price = ((global_gold * usd * 8.133) * 1.085)
    diff = s - fair_price

    if diff < -700000:
        signal = "🔵 فرصت خرید عالی (حباب منفی قوی)"
    elif diff < -200000:
        signal = "🟢 مناسب خرید (حباب منفی)"
    elif diff < 300000:
        signal = "🟡 نرمال / صبر کن"
    else:
        signal = "🔴 حباب مثبت زیاد — مناسب فروش"

    return {
        "signal": signal,
        "fair_price": int(fair_price),
        "diff": int(diff)
    }