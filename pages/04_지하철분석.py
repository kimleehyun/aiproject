import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Subway Top10", layout="wide")
st.title("지하철 승하차 Top10 시각화 (2025년 10월)")

# ----------------------------- #
# 파일 업로드
# ----------------------------- #
uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"])
df = None

def read_csv_any_encoding(f):
    enc_list = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin1"]
    for enc in enc_list:
        try:
            f.seek(0)
            return pd.read_csv(f, encoding=enc), enc
        except Exception:
            pass
    return None, None

if uploaded:
    df, enc = read_csv_any_encoding(uploaded)
    if df is None:
        st.error("CSV 파일 읽기 실패: 인코딩 문제")
        st.stop()
else:
    st.stop()

st.info(f"인코딩: {enc}")
st.write("미리보기")
st.dataframe(df.head())

# ----------------------------- #
# 컬럼 자동 탐지
# ----------------------------- #
cols = df.columns.tolist()

def find_col(df_cols, candidate_list):
    df_low = [c.lower().replace(" ", "") for c in df_cols]
    for cand in candidate_list:
        cand_low = cand.lower().replace(" ", "")
        for i, col_low in enumerate(df_low):
            if cand_low in col_low or col_low in cand_low:
                return df_cols[i]
    return None

date_col = find_col(cols, ["date", "일자", "날짜"])
line_col = find_col(cols, ["호선", "line"])
station_col = find_col(cols, ["역명", "역", "station"])
board_col = find_col(cols, ["승차", "board", "boardings"])
alight_col = find_col(cols, ["하차", "alight", "alightings"])

required = [("날짜", date_col), ("호선", line_col), ("역", station_col), ("승차", board_col), ("하차", alight_col)]
miss = [name for name, col in required if col is None]

if miss:
    st.error(f"필수 컬럼 자동 탐지 실패 → {', '.join(miss)}\n CSV 컬럼명을 알려주세요.")
    st.stop()

# ----------------------------- #
# 날짜 변환
# ----------------------------- #
df["parsed_date"] = pd.to_datetime(df[date_col], errors="coerce")
if df["parsed_date"].isna().all():
    st.error("날짜 파싱 실패. 날짜 형식을 확인해주세요.")
    st.stop()

# 숫자 변환
def to_num(s):
    return (
        s.fillna("0")
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .replace("", "0")
        .astype(float)
    )

df["_board"] = to_num(df[board_col])
df["_alight"] = to_num(df[alight_col])
df["_sum"] = df["_board"] + df["_alight"]

# ----------------------------- #
# UI 필터
# ----------------------------- #
selected_date = st.date_input(
    "날짜 선택 (2025년 10월)",
    value=date(2025, 10, 1),
    min_value=date(2025, 10, 1),
    max_value=date(2025, 10, 31)
)

line_list = sorted(df[line_col].astype(str).unique().tolist())
line_option = ["(전체)"] + line_list
selected_line = st.selectbox("호선 선택", line_option, index=0)

mask = (df["parsed_date"].dt.date == selected_date)
if selected_line != "(전체)":
    mask &= (df[line_col].astype(str) == selected_line)

filtered = df[mask]
if filtered.empty:
    st.warning("조건에 해당하는 데이터 없음")
    st.stop()

# ----------------------------- #
# Top10 집계
# ----------------------------- #
agg = (
    filtered.groupby(station_col)["_sum"]
    .sum()
    .reset_index()
    .rename(columns={station_col: "station", "_sum": "total"})
)

top10 = agg.sort_values("total", ascending=False).head(10)
top10 = top10.reset_index(drop=True)

st.subheader(f"{selected_date} / {selected_line} / Top 10")
st.dataframe(top10)

# ----------------------------- #
# 그래디언트 색상 만들기
# ----------------------------- #
def blue_gradient(n):
    if n <= 0:
        return []
    base = np.array([50, 90, 200])
    light = np.array([180, 210, 255])
    out = []
    for i in range(n):
        t = i / max(n - 1, 1)
        rgb = (base * (1 - t) + light * t).astype(int)
        out.append(f"rgba({rgb[0]},{rgb[1]},{rgb[2]},1.0)")
    return out

# 1등 빨강
colors = ["rgba(255,50,50,1.0)"] + blue_gradient(len(top10) - 1)

# Plotly는 bar 거꾸로 그려야 1등이 위로 감
colors_plot = colors[::-1]

# ----------------------------- #
# Plotly 그래프
# ----------------------------- #
fig = go.Figure(
    go.Bar(
        x=top10["total"][::-1],
        y=top10["station"][::-1],
        orientation="h",
        marker=dict(color=colors_plot),
        hovertemplate="%{y}<br>%{x:,}명<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    template="plotly_white",
    margin=dict(l=150, r=40, t=50, b=50),
    xaxis_title="승차 + 하차 합",
    yaxis_title="역"
)

st.plotly_chart(fig, use_container_width=True)
