import math
import yfinance as yf


def _safe_float(value):
    try:
        if value is None:
            return None
        value = float(value)
        if math.isnan(value):
            return None
        return value
    except Exception:
        return None


def fetch_price_data(ticker):
    """
    yfinance로 현재가와 전일종가를 가져옵니다.
    무료/비공식 데이터라 종목에 따라 지연·누락·오류가 있을 수 있습니다.
    """
    try:
        obj = yf.Ticker(ticker)
        price = None
        prev_close = None

        try:
            info = obj.fast_info
            price = _safe_float(getattr(info, "last_price", None))
            prev_close = _safe_float(getattr(info, "previous_close", None))

            if hasattr(info, "get"):
                if price is None:
                    price = _safe_float(info.get("last_price"))
                if prev_close is None:
                    prev_close = _safe_float(info.get("previous_close"))
        except Exception:
            pass

        # 프리/애프터 포함 최신 1분봉을 우선 시도합니다.
        try:
            intraday = obj.history(period="1d", interval="1m", prepost=True)
            if intraday is not None and len(intraday) > 0:
                closes = intraday["Close"].dropna()
                if len(closes) > 0:
                    price = _safe_float(closes.iloc[-1])
        except Exception:
            pass

        if price is None or prev_close is None:
            hist = obj.history(period="5d", interval="1d", prepost=True)
            if hist is not None and len(hist) >= 2:
                closes = hist["Close"].dropna()
                if len(closes) >= 2:
                    prev_close = _safe_float(closes.iloc[-2])
                    price = _safe_float(closes.iloc[-1])
            elif hist is not None and len(hist) == 1:
                closes = hist["Close"].dropna()
                if len(closes) == 1:
                    price = _safe_float(closes.iloc[-1])

        change_percent = None
        if price is not None and prev_close not in (None, 0):
            change_percent = (price - prev_close) / prev_close * 100

        return {
            "ticker": ticker,
            "price": price,
            "prev_close": prev_close,
            "change_percent": change_percent,
            "source": "yfinance",
            "error": None,
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "price": None,
            "prev_close": None,
            "change_percent": None,
            "source": "yfinance",
            "error": str(e),
        }


def fetch_many_price_data(tickers):
    return {ticker: fetch_price_data(ticker) for ticker in tickers}
