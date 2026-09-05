import os
import httpx

_cache = {}


def get_exchange_rate(from_currency: str, to_currency: str = "sgd") -> float:
    key = f"{from_currency}_{to_currency}"
    if key in _cache:
        return _cache[key]

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency.upper()}/{to_currency.upper()}"

    response = httpx.get(url)
    data = response.json()
    rate = data["conversion_rate"]
    _cache[key] = rate
    return rate
