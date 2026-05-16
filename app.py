import pandas as pd
import streamlit as st

from etf_data import ETF_DATA
from calculator import get_all_unique_tickers, calculate_all_etfs, make_interpretation
from price_fetcher import fetch_many_price_data
from kr_price_fetcher import fetch_many_kr_etf_prices
from market_session import get_korea_now, get_market_session

st.set_page_config(page_title="둥이 ETF 예측기", page_icon="📈", layout="wide")

st.title("📈 둥이 ETF 예측기 v0.5.5")
st.caption("ETF 이름을 누르면 바로 아래에 구성종목 등락률이 펼쳐지는 목록형 대시보드입니다.")

st.warning(
    "투자 판단을 대신하는 앱이 아닙니다. 무료/비공식 데이터는 지연·누락·오류가 있을 수 있습니다. "
    "실제 ETF 가격은 환율, 괴리율, 유동성, 호가, 시장 심리에 따라 달라질 수 있습니다."
)

now = get_korea_now()
session = get_market_session(now)
ticker_map = get_all_unique_tickers(ETF_DATA)

if "changes" not in st.session_state:
    st.session_state.changes = {ticker: 0.0 for ticker in ticker_map.keys()}
if "price_data" not in st.session_state:
    st.session_state.price_data = {}
if "kr_price_data" not in st.session_state:
    st.session_state.kr_price_data = {}
if "expanded_etf" not in st.session_state:
    st.session_state.expanded_etf = None
if "auto_loaded_session_key" not in st.session_state:
    st.session_state.auto_loaded_session_key = None


def load_current_mode_data():
    """
    현재 한국시간 기준 모드에 맞춰 데이터를 불러옵니다.
    - 한국장/종가 고정 모드: 한국 ETF 실제 가격 조회
    - 미국장 예측 모드: 미국 구성종목 가격 조회
    """
    if session["mode"] == "kr_price":
        st.session_state.kr_price_data = fetch_many_kr_etf_prices(ETF_DATA)
    else:
        fetched = fetch_many_price_data(list(ticker_map.keys()))
        st.session_state.price_data = fetched

        new_changes = dict(st.session_state.changes)
        for ticker, data in fetched.items():
            if data.get("change_percent") is not None:
                new_changes[ticker] = float(data["change_percent"])
        st.session_state.changes = new_changes


# 앱 접속 시 현재 세션 데이터를 1번 자동으로 불러옵니다.
# 같은 세션에서 새로고침할 때마다 API를 무한 호출하지 않도록 session key로 막습니다.
if st.session_state.auto_loaded_session_key != session["key"]:
    with st.spinner(f"{session['label']} 데이터를 자동으로 불러오는 중입니다. 잠시만 기다려주세요."):
        load_current_mode_data()
        st.session_state.auto_loaded_session_key = session["key"]
    st.rerun()

st.info(f"현재 한국시간: **{now.strftime('%Y-%m-%d %H:%M:%S')}** / 현재 모드: **{session['label']}**")
st.caption(session["description"])

top_buttons = st.columns([1, 1, 1, 3])

with top_buttons[0]:
    if st.button("현재 모드 데이터 다시 불러오기", type="primary"):
        with st.spinner(f"{session['label']} 데이터를 다시 불러오는 중입니다."):
            load_current_mode_data()
            st.session_state.auto_loaded_session_key = session["key"]
        st.rerun()

with top_buttons[1]:
    if st.button("미국 종목 API 불러오기"):
        with st.spinner("미국 구성종목 가격 데이터를 가져오는 중입니다."):
            fetched = fetch_many_price_data(list(ticker_map.keys()))
            st.session_state.price_data = fetched
            new_changes = dict(st.session_state.changes)
            for ticker, data in fetched.items():
                if data.get("change_percent") is not None:
                    new_changes[ticker] = float(data["change_percent"])
            st.session_state.changes = new_changes
        st.rerun()

with top_buttons[2]:
    if st.button("입력값 초기화"):
        st.session_state.changes = {ticker: 0.0 for ticker in ticker_map.keys()}
        st.session_state.price_data = {}
        st.session_state.kr_price_data = {}
        st.session_state.auto_loaded_session_key = None
        st.rerun()

changes = st.session_state.changes
price_data = st.session_state.price_data
kr_price_data = st.session_state.kr_price_data

us_summary_df, detail_tables = calculate_all_etfs(ETF_DATA, changes, price_data)


def make_kr_summary_df():
    rows = []
    for etf_name, etf_info in ETF_DATA.items():
        data = kr_price_data.get(etf_name, {})
        change_percent = data.get("change_percent")
        price = data.get("price")
        rows.append({
            "ETF명": etf_name,
            "한국코드": etf_info.get("kr_code"),
            "현재가/종가": price if price is not None else "-",
            "예상 등락률(%)": change_percent if change_percent is not None else 0.0,
            "상태": "실제 한국장 반영" if session["key"] == "kr_regular" else "한국 종가 고정",
            "최대 영향 종목": "-",
            "계산방식": session["label"],
            "데이터": data.get("source", "-"),
        })
    return pd.DataFrame(rows).sort_values(by="예상 등락률(%)", ascending=False)


summary_df = make_kr_summary_df() if session["mode"] == "kr_price" else us_summary_df

st.subheader("오늘의 ETF 예측 목록")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("등록 ETF", f"{len(ETF_DATA)}개")
with col2:
    st.metric("입력 대상 티커", f"{len(ticker_map)}개")
with col3:
    if session["mode"] == "kr_price":
        success_count = sum(1 for v in kr_price_data.values() if v.get("price") is not None)
        st.metric("한국 ETF 수집 성공", f"{success_count}/{len(ETF_DATA)}")
    else:
        success_count = sum(1 for v in price_data.values() if v.get("price") is not None)
        st.metric("미국 종목 수집 성공", f"{success_count}/{len(ticker_map)}")
with col4:
    top_etf = summary_df.iloc[0]
    st.metric("현재 1위", top_etf["ETF명"], f"{float(top_etf['예상 등락률(%)']):.2f}%")

view_mode = st.radio("보기 방식", ["전체", "상승 예상", "하락 예상"], horizontal=True)

display_df = summary_df.copy()
if view_mode == "상승 예상":
    display_df = display_df[display_df["예상 등락률(%)"] > 0]
elif view_mode == "하락 예상":
    display_df = display_df[display_df["예상 등락률(%)"] < 0]

styled_df = display_df.copy()
styled_df["예상 등락률(%)"] = styled_df["예상 등락률(%)"].map(lambda x: f"{float(x):.2f}%")

st.caption("아래 목록에서 ETF 이름을 누르면 바로 아래에 구성종목 등락률 표가 펼쳐집니다.")

# 표처럼 보이는 클릭형 목록 헤더
header_cols = st.columns([3, 1.4, 1.4, 2.2, 1.8])
header_cols[0].markdown("**ETF명**")
header_cols[1].markdown("**예상 등락률**")
header_cols[2].markdown("**상태**")
header_cols[3].markdown("**최대 영향 종목**")
header_cols[4].markdown("**계산방식**")

st.divider()

for idx, row in display_df.reset_index(drop=True).iterrows():
    etf_name = row["ETF명"]
    predicted = float(row["예상 등락률(%)"])
    status = row.get("상태", "")
    top_driver = row.get("최대 영향 종목", "-")
    calc_method = row.get("계산방식", "-")

    sign = "▲" if predicted > 0 else "▼" if predicted < 0 else "━"
    row_cols = st.columns([3, 1.4, 1.4, 2.2, 1.8])

    button_label = f"{sign} {etf_name}"
    if row_cols[0].button(button_label, key=f"toggle_{etf_name}", use_container_width=True):
        if st.session_state.expanded_etf == etf_name:
            st.session_state.expanded_etf = None
        else:
            st.session_state.expanded_etf = etf_name
        st.rerun()

    row_cols[1].write(f"{predicted:.2f}%")
    row_cols[2].write(status)
    row_cols[3].write(top_driver)
    row_cols[4].write(calc_method)

    if st.session_state.expanded_etf == etf_name:
        st.markdown(f"#### {etf_name} 구성종목 상세")

        if session["mode"] == "kr_price":
            kr_data = kr_price_data.get(etf_name, {})
            st.info(
                f"한국 ETF 실제 가격 기준: 현재가/종가 {kr_data.get('price', '-')}원, "
                f"등락률 {float(kr_data.get('change_percent') or 0.0):.2f}%, "
                f"데이터 {kr_data.get('source', '-')}"
            )
            st.caption("한국장 모드에서도 아래 구성종목 표는 미국장 예측 참고용입니다.")

        detail_df_for_row = detail_tables.get(etf_name)
        if detail_df_for_row is not None and not detail_df_for_row.empty:
            st.dataframe(detail_df_for_row, use_container_width=True, hide_index=True)
        else:
            st.write("구성종목 상세 데이터가 없습니다.")

        st.divider()

st.divider()

st.divider()

with st.expander("종목별 등락률 입력/수정하기", expanded=False):
    st.write("미국장 예측용 입력값입니다. API 값이 이상하거나 누락된 종목은 여기서 직접 수정할 수 있습니다.")
    cols = st.columns(2)
    new_changes = {}
    for idx, (ticker, name) in enumerate(ticker_map.items()):
        api_data = price_data.get(ticker, {})
        price = api_data.get("price")
        prev_close = api_data.get("prev_close")
        label_extra = ""
        if price is not None:
            label_extra += f" / 현재가 {price:.2f}"
        if prev_close is not None:
            label_extra += f" / 전일 {prev_close:.2f}"
        with cols[idx % 2]:
            new_changes[ticker] = st.number_input(
                label=f"{ticker} / {name}{label_extra}",
                value=float(st.session_state.changes.get(ticker, 0.0)),
                step=0.1,
                format="%.2f",
                key=f"input_{ticker}",
            )
    if st.button("입력값 반영해서 예측 목록 새로 계산하기"):
        st.session_state.changes = new_changes
        st.rerun()

with st.expander("한국 ETF 가격 수집 결과 보기", expanded=False):
    rows = []
    for etf_name, data in kr_price_data.items():
        rows.append({
            "ETF명": etf_name,
            "코드": ETF_DATA[etf_name].get("kr_code"),
            "현재가/종가": data.get("price"),
            "전일대비": data.get("change"),
            "등락률(%)": data.get("change_percent"),
            "데이터": data.get("source"),
            "에러": data.get("error"),
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.write("아직 한국 ETF 가격 데이터를 불러오지 않았습니다.")

with st.expander("미국 종목 API 수집 결과 보기", expanded=False):
    rows = []
    for ticker, data in price_data.items():
        rows.append({"티커": ticker, "현재가": data.get("price"), "전일종가": data.get("prev_close"), "등락률(%)": data.get("change_percent"), "에러": data.get("error")})
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.write("아직 미국 종목 API를 실행하지 않았습니다.")

with st.expander("현재 등록된 ETF 목록", expanded=False):
    st.write(", ".join(ETF_DATA.keys()))
