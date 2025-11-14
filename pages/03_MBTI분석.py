import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="국가별 MBTI 분석", layout="wide")

st.title("🌍 국가별 MBTI 비율 시각화 대시보드")
st.write("국가를 선택하면 MBTI 16유형의 비율을 인터랙티브 막대 그래프로 보여줍니다.")

# CSV 업로드
uploaded = st.file_uploader("MBTI 데이터를 업로드하세요 (CSV)", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)

    # 국가 리스트
    countries = df["Country"].unique()

    # 국가 선택
    selected_country = st.selectbox("국가를 선택하세요", countries)

    # 선택한 나라 데이터
    row = df[df["Country"] == selected_country].iloc[0]

    # MBTI 컬럼만 추출
    mbti_cols = [c for c in df.columns if c != "Country"]
    values = row[mbti_cols].values

    # 데이터프레임 변환
    plot_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "Value": values
    }).sort_values("Value", ascending=False)

    # 색상 생성
    # 1등 → 빨강 / 그 외 → 파랑 색상 그라데이션
    colors = []
    for i in range(len(plot_df)):
        if i == 0:
            colors.append("red")
        else:
            # 파란색 계열 (점점 흐려지는 그라데이션)
            alpha = 1 - (i / len(plot_df)) * 0.85  # 0.15 ~ 1.0
            colors.append(f"rgba(0, 0, 255, {alpha})")

    # Plotly 막대 그래프
    fig = px.bar(
        plot_df,
        x="MBTI",
        y="Value",
        title=f"{selected_country} MBTI 비율",
    )

    # 색 적용
    fig.update_traces(marker_color=colors)

    fig.update_layout(
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font_size=22,
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("CSV 파일을 업로드하면 그래프가 표시됩니다.")
