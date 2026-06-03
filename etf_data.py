"""
ETF 구성종목/비중/보유주식수 데이터 저장 파일입니다.

v0.5.7 two-etfs
- KODEX 미국AI전력핵심인프라
- TIGER 미국우주테크

원칙
- weight: 기준 시점 구성비중(%). 최신 제공 자료에 비중이 없으면 0으로 둡니다.
- shares: ETF 실제 보유주식수. 있으면 실시간 가격과 곱해서 실시간 비중을 재계산합니다.
- CASH_KRW: 원화현금. 등락률은 0%로 처리합니다.
"""

ETF_DATA = {
    "KODEX 미국AI전력핵심인프라": {
        "kr_code": "487230",
        "description": "국내 상장 미국 AI 전력 핵심 인프라 ETF",
        "holdings": [
            {"ticker": "CCJ", "name": "Cameco", "weight": 0, "shares": 616.00},
            {"ticker": "VRT", "name": "Vertiv", "weight": 0, "shares": 412.00},
            {"ticker": "BE", "name": "Bloom Energy", "weight": 0, "shares": 366.00},
            {"ticker": "OKLO", "name": "Oklo", "weight": 0, "shares": 298.00},
            {"ticker": "MTZ", "name": "MasTec", "weight": 0, "shares": 164.00},
            {"ticker": "GEV", "name": "GE Vernova", "weight": 0, "shares": 143.00},
            {"ticker": "POWL", "name": "Powell Industries", "weight": 0, "shares": 140.00},
            {"ticker": "PWR", "name": "Quanta Services", "weight": 0, "shares": 137.00},
            {"ticker": "FIX", "name": "Comfort Systems USA", "weight": 0, "shares": 70.00},
            {"ticker": "STRL", "name": "Sterling Infrastructure", "weight": 0, "shares": 70.00},
            {"ticker": "CASH_KRW", "name": "원화현금", "weight": 0, "shares": None, "is_cash": True, "cash_value": 2543371},
        ],
    },
    "TIGER 미국우주테크": {
        "kr_code": "0183J0",
        "description": "국내 상장 미국 우주테크 ETF",
        "holdings": [
            {"ticker": "RDW", "name": "Redwire", "weight": 0, "shares": 5684.00},
            {"ticker": "LUNR", "name": "Intuitive Machines", "weight": 0, "shares": 2603.00},
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 0, "shares": 881.00},
            {"ticker": "PL", "name": "Planet Labs", "weight": 0, "shares": 807.00},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 0, "shares": 583.00},
            {"ticker": "VOYG", "name": "Voyager Technologies", "weight": 0, "shares": 413.00},
            {"ticker": "GSAT", "name": "Globalstar", "weight": 0, "shares": 339.00},
            {"ticker": "FLY", "name": "Firefly Aerospace", "weight": 0, "shares": 339.00},
            {"ticker": "SATS", "name": "EchoStar", "weight": 0, "shares": 193.00},
            {"ticker": "KRMN", "name": "Karman Holdings", "weight": 0, "shares": 121.00},
            {"ticker": "CASH_KRW", "name": "원화현금", "weight": 0, "shares": None, "is_cash": True, "cash_value": 2458794},
        ],
    },
}
