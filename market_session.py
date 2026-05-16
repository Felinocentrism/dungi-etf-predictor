from datetime import datetime, time
from zoneinfo import ZoneInfo


def get_korea_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))


def get_market_session(now=None):
    """
    한국시간 기준 세션 구분.

    월요일~금요일
    09:00 ~ 15:30
        → 한국장 실제 ETF 가격 반영

    월요일~금요일
    15:31 ~ 16:59
        → 한국 종가 고정

    월요일~금요일
    17:00 ~ 22:29
        → 미국 프리마켓 기반 예측

    월요일~금요일
    22:30 ~ 익일 04:59
        → 미국 정규장 기반 예측

    화요일~토요일
    05:00 ~ 08:59
        → 미국 애프터마켓 기반 예측

    토요일 09:00 ~ 월요일 08:59
        → 미국 금요일 애프터마켓 기반 예측
    """
    if now is None:
        now = get_korea_now()

    t = now.time()
    weekday = now.weekday()
    # Python weekday:
    # Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6

    # 토요일 09:00 이후 ~ 일요일 전체
    if weekday == 5 and t >= time(9, 0):
        return {
            "key": "weekend_friday_aftermarket",
            "label": "미국 금요일 애프터마켓 기반 예측",
            "mode": "us_constituents",
            "description": "토요일 09:00~월요일 08:59: 미국 금요일 애프터마켓 기준 예측값을 유지합니다.",
        }

    if weekday == 6:
        return {
            "key": "weekend_friday_aftermarket",
            "label": "미국 금요일 애프터마켓 기반 예측",
            "mode": "us_constituents",
            "description": "토요일 09:00~월요일 08:59: 미국 금요일 애프터마켓 기준 예측값을 유지합니다.",
        }

    # 월요일 00:00~08:59
    if weekday == 0 and t < time(9, 0):
        return {
            "key": "weekend_friday_aftermarket",
            "label": "미국 금요일 애프터마켓 기반 예측",
            "mode": "us_constituents",
            "description": "토요일 09:00~월요일 08:59: 미국 금요일 애프터마켓 기준 예측값을 유지합니다.",
        }

    # 월요일~금요일 한국장
    if weekday in [0, 1, 2, 3, 4] and time(9, 0) <= t <= time(15, 30):
        return {
            "key": "kr_regular",
            "label": "한국장 실시간 가격 반영",
            "mode": "kr_price",
            "description": "월~금 09:00~15:30: 한국 ETF의 실제 시장 가격 변동률을 표시합니다.",
        }

    # 월요일~금요일 한국 종가 고정
    if weekday in [0, 1, 2, 3, 4] and time(15, 31) <= t < time(17, 0):
        return {
            "key": "kr_close_fixed",
            "label": "한국 종가 고정",
            "mode": "kr_price",
            "description": "월~금 15:31~17:00: 한국 ETF 종가 기준 변동률을 고정 표시합니다.",
        }

    # 월요일~금요일 미국 프리마켓
    if weekday in [0, 1, 2, 3, 4] and time(17, 0) <= t < time(22, 30):
        return {
            "key": "us_premarket",
            "label": "미국 프리마켓 기반 예측",
            "mode": "us_constituents",
            "description": "월~금 17:00~22:29: 미국 프리마켓 가격을 가능한 범위에서 반영해 예측합니다.",
        }

    # 월요일~금요일 밤 22:30~23:59 미국 정규장
    if weekday in [0, 1, 2, 3, 4] and t >= time(22, 30):
        return {
            "key": "us_regular",
            "label": "미국 정규장 기반 예측",
            "mode": "us_constituents",
            "description": "월~금 22:30~익일 05:00: 미국 정규장 가격을 반영해 예측합니다.",
        }

    # 화요일~토요일 새벽 00:00~04:59 미국 정규장
    if weekday in [1, 2, 3, 4, 5] and t < time(5, 0):
        return {
            "key": "us_regular",
            "label": "미국 정규장 기반 예측",
            "mode": "us_constituents",
            "description": "월~금 22:30~익일 05:00: 미국 정규장 가격을 반영해 예측합니다.",
        }

    # 화요일~토요일 05:00~08:59 미국 애프터마켓
    if weekday in [1, 2, 3, 4, 5] and time(5, 0) <= t < time(9, 0):
        return {
            "key": "us_aftermarket",
            "label": "미국 애프터마켓 기반 예측",
            "mode": "us_constituents",
            "description": "화~토 05:00~08:59: 미국 애프터마켓 가격을 가능한 범위에서 반영해 예측합니다.",
        }

    # 안전장치: 정의되지 않은 시간은 미국 구성종목 기반 예측으로 처리
    return {
        "key": "us_constituents_fallback",
        "label": "미국 구성종목 기반 예측",
        "mode": "us_constituents",
        "description": "예외 시간대입니다. 미국 구성종목 가격 기반으로 예측합니다.",
    }
