"""
ETF 구성종목/비중/보유주식수 데이터 저장 파일입니다.

- weight: 기준 시점 구성비중(%)
- shares: ETF 실제 보유주식수. 있으면 실시간 가격과 곱해서 실시간 비중을 재계산합니다.
- CASH_KRW: 원화현금. 등락률은 0%로 처리합니다.
"""

ETF_DATA = {
    "TIGER 미국우주테크": {
        "kr_code": "0183J0",
        "description": "국내 상장 미국 우주테크 ETF",
        "holdings": [
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 30.53, "shares": 1136.00},
            {"ticker": "LUNR", "name": "Intuitive Machines", "weight": 17.41, "shares": 2360.30},
            {"ticker": "RDW", "name": "Redwire", "weight": 14.52, "shares": 5153.70},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 10.10, "shares": 528.63},
            {"ticker": "PL", "name": "Planet Labs", "weight": 7.27, "shares": 731.43},
            {"ticker": "GSAT", "name": "Globalstar", "weight": 6.43, "shares": 307.78},
            {"ticker": "SATS", "name": "EchoStar", "weight": 5.65, "shares": 174.63},
            {"ticker": "FLY", "name": "Firefly Aerospace", "weight": 3.10, "shares": 307.75},
            {"ticker": "SPCE", "name": "Virgin Galactic", "weight": 2.83, "shares": 374.58},
            {"ticker": "KRMN", "name": "Karman Holdings", "weight": 1.69, "shares": 109.45},
        ],
    },
    "KODEX 미국우주항공": {
        "kr_code": "0167Z0",
        "description": "국내 상장 미국 우주항공 ETF",
        "holdings": [
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 26.36, "shares": 959.70},
            {"ticker": "LUNR", "name": "Intuitive Machines", "weight": 11.69, "shares": 1550.20},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 11.29, "shares": 577.95},
            {"ticker": "SATS", "name": "EchoStar", "weight": 7.39, "shares": 223.40},
            {"ticker": "PL", "name": "Planet Labs", "weight": 6.83, "shares": 672.20},
            {"ticker": "BA", "name": "Boeing", "weight": 3.67, "shares": 59.38},
            {"ticker": "HWM", "name": "Howmet Aerospace", "weight": 3.60, "shares": 51.20},
            {"ticker": "TDG", "name": "TransDigm Group", "weight": 3.28, "shares": 10.30},
            {"ticker": "GE", "name": "GE Aerospace", "weight": 3.14, "shares": 40.68},
            {"ticker": "KTOS", "name": "Kratos Defense & Security", "weight": 2.97, "shares": 197.07},
        ],
    },
    "ACE 미국우주테크액티브": {
        "kr_code": "0180V0",
        "description": "국내 상장 미국 우주테크 액티브 ETF",
        "holdings": [
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 26.42, "shares": 985.00},
            {"ticker": "SATS", "name": "EchoStar", "weight": 21.47, "shares": 664.00},
            {"ticker": "RDW", "name": "Redwire", "weight": 4.36, "shares": 1550.00},
            {"ticker": "LUNR", "name": "Intuitive Machines", "weight": 4.24, "shares": 576.00},
            {"ticker": "MDA.TO", "name": "MDA Space", "weight": 4.07, "shares": 463.00},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 3.91, "shares": 205.00},
            {"ticker": "FLY", "name": "Firefly Aerospace", "weight": 3.90, "shares": 387.00},
            {"ticker": "PL", "name": "Planet Labs", "weight": 3.90, "shares": 333.00},
            {"ticker": "STEL", "name": "Stellar", "weight": 3.90, "shares": 2030.00},
            {"ticker": "TSAT", "name": "Telesat", "weight": 3.89, "shares": 280.00},
        ],
    },
    "SOL 미국우주항공TOP10": {
        "kr_code": "0181L0",
        "description": "국내 상장 미국 우주항공 TOP10 ETF",
        "holdings": [
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 30.90, "shares": 1038.00},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 12.60, "shares": 594.75},
            {"ticker": "SATS", "name": "EchoStar", "weight": 10.26, "shares": 341.64},
            {"ticker": "PL", "name": "Planet Labs", "weight": 9.67, "shares": 877.67},
            {"ticker": "VSAT", "name": "Viasat", "weight": 8.38, "shares": 424.39},
            {"ticker": "GSAT", "name": "Globalstar", "weight": 8.35, "shares": 360.31},
            {"ticker": "FLY", "name": "Firefly Aerospace", "weight": 6.87, "shares": 613.00},
            {"ticker": "LUNR", "name": "Intuitive Machines", "weight": 6.45, "shares": 789.67},
            {"ticker": "IRDM", "name": "Iridium Communications", "weight": 2.25, "shares": 192.25},
            {"ticker": "RDW", "name": "Redwire", "weight": 1.96, "shares": 627.39},
        ],
    },
    "1Q 미국 우주항공테크": {
        "kr_code": "0131V0",
        "description": "국내 상장 미국 우주항공테크 ETF",
        "holdings": [
            {"ticker": "RKLB", "name": "Rocket Lab", "weight": 22.23, "shares": 977.00},
            {"ticker": "JOBY", "name": "Joby Aviation", "weight": 15.90, "shares": 6781.00},
            {"ticker": "GE", "name": "GE Aerospace", "weight": 8.84, "shares": 138.00},
            {"ticker": "VRT", "name": "Vertiv", "weight": 8.60, "shares": 135.00},
            {"ticker": "FLY", "name": "Firefly Aerospace", "weight": 7.96, "shares": 260.00},
            {"ticker": "SATS", "name": "EchoStar", "weight": 7.35, "shares": 268.00},
            {"ticker": "ACHR", "name": "Archer Aviation", "weight": 6.58, "shares": 470.00},
            {"ticker": "ASTS", "name": "AST SpaceMobile", "weight": 6.13, "shares": 379.00},
            {"ticker": "HON", "name": "Honeywell International", "weight": 3.17, "shares": 69.00},
            {"ticker": "RTX", "name": "RTX", "weight": 3.07, "shares": 81.00},
        ],
    },
    "KODEX 미국AI전력핵심인프라": {
        "kr_code": "487230",
        "description": "국내 상장 미국 AI 전력 핵심 인프라 ETF",
        "holdings": [
            {"ticker": "BE", "name": "Bloom Energy", "weight": 18.13, "shares": 580.55},
            {"ticker": "VRT", "name": "Vertiv", "weight": 18.04, "shares": 452.46},
            {"ticker": "GEV", "name": "GE Vernova", "weight": 15.41, "shares": 134.60},
            {"ticker": "PWR", "name": "Quanta Services", "weight": 11.79, "shares": 141.40},
            {"ticker": "CCJ", "name": "Cameco", "weight": 9.61, "shares": 772.84},
            {"ticker": "MTZ", "name": "MasTec", "weight": 8.42, "shares": 184.53},
            {"ticker": "STRL", "name": "Sterling Infrastructure", "weight": 8.38, "shares": 91.08},
            {"ticker": "VST", "name": "Vistra", "weight": 6.61, "shares": 430.49},
            {"ticker": "OKLO", "name": "Oklo", "weight": 2.26, "shares": 301.50},
            {"ticker": "SMR", "name": "NuScale Power", "weight": 1.10, "shares": 857.77},
            {"ticker": "CASH_KRW", "name": "원화현금", "weight": 0.19, "shares": None, "is_cash": True, "cash_value": 2748.01},
        ],
    },
}
