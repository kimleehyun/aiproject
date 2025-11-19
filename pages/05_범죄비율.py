import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="범죄 데이터 분석", layout="wide")
st.title("📊 지역별 범죄 비율 분석 대시보드")

# 🔹 여러 인코딩 자동 시도
encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
df = None

for enc in encodings:
    try:
        df = pd.read_csv("crime.csv", encoding=enc)
        break
    except:
        pass

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# 🔹 지역(컬럼명) 목록 생성 — '범죄대분류', '범죄중분류' 제외
region_cols = [col for col in df.columns if col not in ["범죄대분류", "범죄중분류"]]

selected_region = st.selectbox("지역을 선택하세요", region_cols)

# 🔹 선택한 지역의 값만 추출
crime_df = pd.DataFrame({
    "범죄유형": df["범죄중분류"],
    "비율": df[selected_region]
}).sort_values("비율", ascending=False)

# 🔹 색상 구성: 1등은 빨강 + 나머지 블루 그라데이션 (자동 확장)
base_colors = px.colors.sequential.Blues
needed = len(crime_df) - 1

# 색 개수가 부족하면 반복해서 색 리스트 늘리기
expanded_colors = (base_colors * ((needed // len(base_colors)) + 1))[:needed]

colors = ["red"] + expanded_colors

# 🔹 인터랙티브 그래프 생성
fig = go.Figure([
    go.Bar(
        x=crime_df["범죄유형"],
        y=crime_df["비율"],
        marker=dict(color=colors)
    )
])

fig.update_layout(
    title=f"📍 {selected_region} 지역 범죄 비율",
    xaxis_title="범죄 유형",
    yaxis_title="비율(건수)",
    template="plotly_white",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("📄 데이터 확인"):
    st.dataframe(crime_df)
