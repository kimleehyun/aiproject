import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="범죄 데이터 분석", layout="wide")

st.title("📊 지역별 범죄 비율 분석 대시보드")

# 여러 인코딩 자동 시도
encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr", "latin1"]

df = None
for enc in encodings:
    try:
        df = pd.read_csv("crime.csv", encoding=enc)
        st.success(f"CSV 파일 인코딩 자동 감지 성공: {enc}")
        break
    except Exception:
        pass

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다. 인코딩을 확인하세요.")
    st.stop()

# 지역 선택
regions = df["지역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 선택 지역 데이터
selected = df[df["지역"] == selected_region].drop(columns=["지역"])

# 데이터 정리
crime_values = selected.iloc[0]
crime_df = pd.DataFrame({
    "범죄유형": crime_values.index,
    "비율": crime_values.values
})
crime_df = crime_df.sort_values("비율", ascending=False).reset_index(drop=True)

# 색상 (1등 빨강, 나머지 블루 그라데이션)
colors = ["red"] + px.colors.sequential.Blues[len(crime_df) - 1]

# 그래프
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
    yaxis_title="비율(%)",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("📄 데이터 확인"):
    st.dataframe(crime_df)
