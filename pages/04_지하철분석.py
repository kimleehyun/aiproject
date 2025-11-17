import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로드 — pages 폴더여도 이렇게 해야 불러와짐
df = pd.read_csv("subway.csv", encoding="utf-8")

st.title("2025년 10월 지하철 승차·하차 TOP10 역 분석")

# 날짜 선택
date_list = sorted(df["날짜"].unique())
selected_date = st.selectbox("날짜 선택", date_list)

# 호선 선택
line_list = sorted(df["호선"].unique())
selected_line = st.selectbox("호선 선택", line_list)

# 필터링
filtered = df[(df["날짜"] == selected_date) & (df["호선"] == selected_line)].copy()

# 승차 + 하차 총합 컬럼 생성
filtered["총이용객"] = filtered["승차"] + filtered["하차"]

# TOP10 추출
top10 = filtered.sort_values("총이용객", ascending=False).head(10)

# 색상 설정 (1등 빨강, 나머지는 파랑 → 하늘색 그라데이션)
colors = ["red"] + [f"rgba(0, 102, 255, {1 - i*0.08})" for i in range(1, 10)]

# Plotly로 시각화
fig = px.bar(
    top10,
    x="역명",
    y="총이용객",
    title=f"{selected_date} / {selected_line} 승차+하차 TOP10",
)

fig.update_traces(marker_color=colors)

st.plotly_chart(fig, use_container_width=True)
