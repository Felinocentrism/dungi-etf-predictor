import pandas as pd


def get_all_unique_tickers(etf_data):
    ticker_map = {}
    for etf_info in etf_data.values():
        for item in etf_info["holdings"]:
            # CASH_KRW 같은 현금 항목은 API 조회 대상에서 제외합니다.
            if item.get("is_cash"):
                continue
            ticker_map.setdefault(item["ticker"], item["name"])
    return ticker_map


def _can_use_shares(holdings, price_data):
    for item in holdings:
        if item.get("is_cash"):
            continue
        shares = item.get("shares")
        ticker = item["ticker"]
        price = price_data.get(ticker, {}).get("price")
        if shares is None or price is None:
            return False
    return True


def _dynamic_weights_from_shares(holdings, price_data):
    market_values = {}
    total_value = 0.0

    for item in holdings:
        ticker = item["ticker"]

        if item.get("is_cash"):
            value = float(item.get("cash_value", 0.0))
        else:
            shares = float(item.get("shares") or 0)
            price = price_data.get(ticker, {}).get("price")
            value = shares * float(price) if price is not None else 0.0

        market_values[ticker] = value
        total_value += value

    weights = {
        ticker: (value / total_value * 100) if total_value > 0 else 0.0
        for ticker, value in market_values.items()
    }
    return weights, market_values


def calculate_single_etf(holdings, changes, price_data=None):
    if price_data is None:
        price_data = {}

    use_shares = _can_use_shares(holdings, price_data)
    dynamic_weights = {}
    market_values = {}

    if use_shares:
        dynamic_weights, market_values = _dynamic_weights_from_shares(holdings, price_data)

    rows = []
    total_prediction = 0.0

    for item in holdings:
        ticker = item["ticker"]
        stored_weight = float(item["weight"])
        shares = item.get("shares")

        if item.get("is_cash"):
            price = "-"
            prev_close = "-"
            source = "cash"
            change_percent = 0.0
        else:
            price = price_data.get(ticker, {}).get("price")
            prev_close = price_data.get(ticker, {}).get("prev_close")
            source = price_data.get(ticker, {}).get("source", "manual")
            change_percent = float(changes.get(ticker, 0.0))

        calc_weight = dynamic_weights.get(ticker, stored_weight) if use_shares else stored_weight
        contribution = change_percent * (calc_weight / 100)
        total_prediction += contribution

        rows.append({
            "티커": ticker,
            "종목명": item["name"],
            "보유주식수": shares if shares is not None else "-",
            "현재가": price if price is not None else "-",
            "전일종가": prev_close if prev_close is not None else "-",
            "기준비중(%)": stored_weight,
            "계산비중(%)": calc_weight,
            "등락률(%)": change_percent,
            "ETF 기여도(%p)": contribution,
            "계산방식": "보유주식수×현재가" if use_shares else "기준비중",
            "데이터": source,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="ETF 기여도(%p)", key=lambda col: col.abs(), ascending=False)

    return total_prediction, df, use_shares


def calculate_all_etfs(etf_data, changes, price_data=None):
    if price_data is None:
        price_data = {}

    summary_rows = []
    detail_tables = {}

    for etf_name, etf_info in etf_data.items():
        prediction, detail_df, use_shares = calculate_single_etf(etf_info["holdings"], changes, price_data)
        detail_tables[etf_name] = detail_df

        top_driver = "-"
        if not detail_df.empty:
            non_cash_df = detail_df[detail_df["티커"] != "CASH_KRW"]
            if not non_cash_df.empty:
                top_row = non_cash_df.iloc[0]
                top_driver = f"{top_row['티커']} ({top_row['ETF 기여도(%p)']:.2f}%p)"

        summary_rows.append({
            "ETF명": etf_name,
            "예상 등락률(%)": prediction,
            "상태": make_status(prediction),
            "최대 영향 종목": top_driver,
            "계산방식": "보유주식수 기반" if use_shares else "기준비중 기반",
        })

    summary_df = pd.DataFrame(summary_rows).sort_values(by="예상 등락률(%)", ascending=False)
    return summary_df, detail_tables


def make_status(prediction):
    if prediction >= 2:
        return "강한 상승"
    if prediction >= 0.7:
        return "상승"
    if prediction > -0.7:
        return "보합권"
    if prediction > -2:
        return "하락"
    return "강한 하락"


def make_interpretation(prediction):
    return f"구성종목 움직임만 보면 {make_status(prediction)} 출발 가능성이 있습니다."
