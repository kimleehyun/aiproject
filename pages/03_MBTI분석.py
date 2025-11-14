import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="국가별 MBTI 분석", layout="wide")

st.title("🌍 국가별 MBTI 분석 대시보드")

# CSV 업로드
uploaded = st.file_uploader("MBTI 데이터를 업로드하세요 (CSV)", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)

    # MBTI 목록
    mbti_cols = [c for c in df.columns if c != "Country"]

    # --- 탭 구성 ---
    tab1, tab2 = st.tabs(["국가별 MBTI 비율 보기", "MBTI 유형별 Top 10 국가"])

    # ================================
    # TAB 1: 국가 선택 후 MBTI 비율 시각화
    # ================================
    with tab1:
        st.subheader("📌 선택한 국가의 MBTI 비율 시각화")

        countries = df["Country"].unique()
        selected_country = st.selectbox("국가를 선택하세요", countries)

        row = df[df["Country"] == selected_country].iloc[0]
        values = row[mbti_cols].values

        plot_df = pd.DataFrame({
            "MBTI": mbti_cols,
            "Value": values
        }).sort_values("Value", ascending=False)

        # 색상 생성 — 1등 빨강, 나머지 파랑 그라데이션
        colors = []
        for i in range(len(plot_df)):
            if i == 0:
                colors.append("red")
            else:
                alpha = 1 - (i / len(plot_df)) * 0.85
                colors.append(f"rgba(0, 0, 255, {alpha})")

        fig = px.bar(
            plot_df,
            x="MBTI",
            y="Value",
            title=f"{selected_country} MBTI 비율",
        )

        fig.update_traces(marker_color=colors)
        fig.update_layout(
            xaxis_title="MBTI 유형",
            yaxis_title="비율",
            plot_bgcolor="white",
            paper_bgcolor="white",
            title_font_size=22,
        )

        st.plotly_chart(fig, use_container_width=True)

    # ================================
    # TAB 2: 선택한 MBTI 기준 Top 10 국가
    # ================================
    with tab2:
        st.subheader("📌 MBTI 유형 선택 → 세계 Top 10 국가")

        selected_mbti = st.selectbox("MBTI 유형을 선택하세요", mbti_cols)

        top10 = df.sort_values(selected_mbti, ascending=False).head(10)

        # 색상 지정: 한국은 빨간색, 나머지는 파란색 그라데이션
        colors = []
        for idx, row in top10.iterrows():
            if row["Country"] == "South Korea" or row["Country"] == "Korea" or row["Country"] == "Republic of Korea":
                colors.append("red")
            else:
                # 파란색 그라데이션
                rank = top10[selected_mbti].rank(ascending=False)[idx] - 1
                alpha = 1 - (rank / 10) * 0.85
                colors.append(f"rgba(0, 0, 255, {alpha})")

        fig2 = px.bar(
            top10,
            x="Country",
            y=selected_mbti,
            title=f"MBTI {selected_mbti} 비율 Top 10 국가",
        )

        fig2.update_traces(marker_color=colors)
        fig2.update_layout(
            xaxis_title="국가",
            yaxis_title=f"{selected_mbti} 비율",
            plot_bgcolor="white",
            paper_bgcolor="white",
            title_font_size=22,
        )

        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("CSV 파일을 업로드하면 두 탭 모두 활성화됩니다!")

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("CSV 파일을 업로드하면 그래프가 표시됩니다.")
