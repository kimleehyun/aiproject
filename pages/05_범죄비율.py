# 기본 설정
st.set_page_config(page_title="범죄 데이터 분석", layout="wide")

st.title("📊 지역별 범죄 비율 분석 대시보드")

# CSV 읽기
df = pd.read_csv("crime.csv")

# 지역 목록
regions = df["지역"].unique()

# 지역 선택 UI
selected_region = st.selectbox("지역을 선택하세요", regions)

# 선택 지역 데이터
filtered = df[df["지역"] == selected_region].drop(columns=["지역"])

# 범죄 유형별 비율 데이터 변환
crime_values = filtered.iloc[0]
crime_df = pd.DataFrame({
    "범죄유형": crime_values.index,
    "비율": crime_values.values
})

# 내림차순 정렬
crime_df = crime_df.sort_values(by="비율", ascending=False).reset_index(drop=True)

# 색상 구성: 1등은 빨간색, 나머지는 블루 그라데이션
colors = ["red"] + px.colors.sequential.Blues[len(crime_df) - 1]

# Plotly 그래프
fig = go.Figure(data=[
    go.Bar(
        x=crime_df["범죄유형"],
        y=crime_df["비율"],
        marker=dict(color=colors)
    )
])

fig.update_layout(
    title=f"📍 {selected_region} 지역 범죄 비율",
    xaxis_title="범죄 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=600
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 원본 데이터확인 (옵션)
with st.expander("📁 원본 데이터 확인"):
    st.dataframe(crime_df)
