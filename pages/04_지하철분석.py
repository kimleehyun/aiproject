# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Subway Top10 (Oct 2025)", layout="wide")

st.title("지하철 승하차 Top10 — 2025년 10월 한 날 선택")
st.caption("파일 업로드하거나 리포지토리 내 'subway.csv'를 사용하세요.")

#
# 파일 로드 (업로드 우선, 없으면 로컬 경로 시도)
#
uploaded = st.file_uploader("CSV 파일 업로드 (UTF-8/CP949 가능)", type=["csv"])
if uploaded is not None:
    try:
        # 시도: utf-8, cp949, euc-kr, utf-8-sig, latin1
        encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig', 'latin1']
        for enc in encodings:
            try:
                uploaded.seek(0)
                df = pd.read_csv(uploaded, encoding=enc)
                used_encoding = enc
                break
            except Exception:
                df = None
        if df is None:
            st.error("업로드된 CSV를 읽는 데 실패했습니다(인코딩 문제).")
            st.stop()
    except Exception as e:
        st.error(f"파일 읽기 실패: {e}")
        st.stop()
else:
    # 로컬 경로 시도
    try:
        df = pd.read_csv("subway.csv", encoding='cp949')
        used_encoding = 'cp949'
    except Exception:
        try:
            df = pd.read_csv("subway.csv", encoding='utf-8')
            used_encoding = 'utf-8'
        except Exception:
            st.warning("업로드된 파일이 없고 로컬 'subway.csv'도 읽을 수 없습니다. 먼저 업로드해주세요.")
            st.stop()

st.sidebar.markdown(f"**읽은 파일 인코딩 추정:** `{used_encoding}`")
st.write("파일 미리보기 (상위 10행)")
st.dataframe(df.head(10), use_container_width=True)

#
# 유연한 컬럼 자동 탐지
#
def find_column(candidates, cols):
    for c in candidates:
        for col in cols:
            if col.lower() == c.lower():
                return col
    # 대소문자/공백 제거 비교
    lowered = {col: col.lower().replace(" ", "").replace("_","") for col in cols}
    for c in candidates:
        key = c.lower().replace(" ", "").replace("_","")
        for orig, norm in lowered.items():
            if key == norm:
                return orig
    # 포함관계 허용 (부분 일치)
    for c in candidates:
        for col in cols:
            if c.lower() in col.lower() or col.lower() in c.lower():
                return col
    return None

cols = df.columns.tolist()

# 날짜 컬럼 후보
date_candidates = ['date', '일자', '날짜', 'day', 'datetime', 'time']
date_col = find_column(date_candidates, cols)
# 호선 컬럼 후보
line_candidates = ['호선', 'line', 'Line', '노선']
line_col = find_column(line_candidates, cols)
# 역 컬럼 후보
station_candidates = ['역', 'station', 'STATION_NAME', 'station_name', '역명', '역 이름']
station_col = find_column(station_candidates, cols)
# 승차/하차 컬럼 후보
board_candidates = ['승차', 'board', 'boarding', '승객수_승차', '승차수']
alight_candidates = ['하차', 'alight', 'alighting', '하차수', '승객수_하차']

board_col = find_column(board_candidates, cols)
alight_col = find_column(alight_candidates, cols)

# 안내 텍스트
st.sidebar.markdown("### 자동 감지된 컬럼")
st.sidebar.write({
    "date_col": date_col,
    "line_col": line_col,
    "station_col": station_col,
    "board_col": board_col,
    "alight_col": alight_col
})

# 필수 컬럼 체크
missing_cols = []
for name, v in (("날짜", date_col), ("호선", line_col), ("역", station_col), ("승차", bo_
