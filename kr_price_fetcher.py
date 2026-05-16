import re
import requests


def _to_float(text):
    if text is None:
        return None
    try:
        text = str(text).replace(",", "").replace("%", "").strip()
        if text in ("", "-", "N/A"):
            return None
        return float(text)
    except Exception:
        return None


def _search_recursive(obj, target_keys):
    if isinstance(obj, dict):
        for key in target_keys:
            if key in obj:
                return obj[key]
        for value in obj.values():
            found = _search_recursive(value, target_keys)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = _search_recursive(value, target_keys)
            if found is not None:
                return found
    return None


def fetch_kr_etf_price(code):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://finance.naver.com/"}
    try:
        url = f"https://polling.finance.naver.com/api/realtime/domestic/stock/{code}"
        res = requests.get(url, headers=headers, timeout=10)
        if res.ok:
            data = res.json()
            price = _search_recursive(data, ["closePrice", "nowVal", "tradePrice", "currentPrice"])
            change = _search_recursive(data, ["compareToPreviousClosePrice", "changePrice"])
            change_rate = _search_recursive(data, ["fluctuationsRatio", "changeRate"])
            price_f = _to_float(price)
            change_f = _to_float(change)
            change_rate_f = _to_float(change_rate)
            if price_f is not None:
                prev_close = price_f - change_f if change_f is not None else None
                return {"code": code, "price": price_f, "change": change_f, "change_percent": change_rate_f, "prev_close": prev_close, "source": "naver_realtime", "error": None}
    except Exception:
        pass

    try:
        url = f"https://finance.naver.com/item/sise.naver?code={code}"
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "euc-kr"
        text = res.text
        price_match = re.search(r'id="_nowVal">([\d,]+)</strong>', text)
        diff_match = re.search(r'id="_diff">\s*<span[^>]*>([\d,]+)</span>', text)
        rate_match = re.search(r'id="_rate">\s*<span[^>]*>([+\-]?[\d.]+)%</span>', text)
        price = _to_float(price_match.group(1)) if price_match else None
        change = _to_float(diff_match.group(1)) if diff_match else None
        change_percent = _to_float(rate_match.group(1)) if rate_match else None
        if price is not None:
            return {"code": code, "price": price, "change": change, "change_percent": change_percent, "prev_close": price - change if change is not None else None, "source": "naver_html", "error": None}
    except Exception as e:
        return {"code": code, "price": None, "change": None, "change_percent": None, "prev_close": None, "source": "naver", "error": str(e)}

    return {"code": code, "price": None, "change": None, "change_percent": None, "prev_close": None, "source": "naver", "error": "가격 조회 실패"}


def fetch_many_kr_etf_prices(etf_data):
    results = {}
    for etf_name, etf_info in etf_data.items():
        code = etf_info.get("kr_code")
        if code:
            results[etf_name] = fetch_kr_etf_price(code)
    return results
