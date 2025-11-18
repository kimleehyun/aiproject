import streamlit as st
import pandas as pd
import plotly.express as px
import io
import base64

def create_crime_ratio_bar_chart(df_data):
    """
    지역별 범죄 총합 비율 막대 그래프를 생성합니다.
    """
    # 1. '범죄대분류', '범죄중분류' 컬럼을 제외하고 지역별 합계를 계산
    df_regional_crime = df_data.drop(columns=['범죄대분류', '범죄중분류'], errors='ignore').sum().reset_index()
    df_regional_crime.columns = ['지역명', '범죄총합']
    
    # 2. 전체 범죄 총합 계산
    total_crime = df_regional_crime['범죄총합'].sum()
    
    # 3. 지역별 범죄 비율 계산
    df_regional_crime['범죄비율'] = (df_regional_crime['범죄총합'] / total_crime) * 100
    
    # 4. 범죄총합 기준으로 내림차순 정렬
    df_ranked = df_regional_crime.sort_values(by='범죄총합', ascending=False).reset_index(drop=True)
    df_ranked['순위'] = df_ranked.index + 1
    
    # 5. 색상 처리: 1등은 빨간색, 나머지는 그라데이션
    
    # 1등 지역 이름
    top_region = df_ranked.iloc[0]['지역명']
    
    # Plotly Express의 'Viridis' 스케일 사용을 위한 기본 색상 리스트 생성
    # 1등은 'red', 나머지는 Viridis 스케일의 색상으로 지정하여 그라데이션 효과
    num_regions = len(df_ranked)
    
    # Plotly 기본 그라데이션 색상 스케일 (예: Viridis)에서 색상을 가져옴
    viridis_colors = px.colors.sequential.Viridis
    
    # 지역 개수에 맞게 색상 리스트를 조정 (사이클링)
    # 1등 지역을 제외한 나머지 지역에 대한 색상 리스트
    gradient_colors = [viridis_colors[i % len(viridis_colors)] for i in range(1, num_regions)]
    
    # 최종 색상 리스트 (1등은 빨간색)
    final_colors = ['red'] + gradient_colors
    
    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        df_ranked,
        x='지역명',
        y='범죄비율',
        text=df_ranked['범죄비율'].round(2).astype(str) + '%', # 막대 위에 비율(%) 표시
        color='범죄비율', # 색상 스케일링을 위한 컬럼 지정 (그라데이션 효과)
        color_continuous_scale=viridis_colors, # 사용할 색상 그라데이션 스케일
        title='🚨 전국 지역별 범죄 발생 비율',
        labels={'지역명': '지역명', '범죄비율': '범죄 비율 (%)'},
        hover_data=['순위', '범죄총합'] # 마우스 오버 시 순위와 총합 표시
    )

    # 1등 막대 색상만 빨간색으로 강제 지정
    # Plotly의 `update_traces`를 사용하여 1등 막대의 색상을 빨간색으로 변경
    for i, region in enumerate(df_ranked['지역명']):
        if region == top_region:
            fig.update_traces(marker_color='red', selector=dict(x=region))
        else:
            # 나머지 막대는 원래의 그라데이션 색상 유지
            pass
            
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'}, # 비율(y축 값)에 따라 내림차순 정렬
        yaxis_title='범죄 비율 (%)',
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        showlegend=False, # 범례 숨김
        coloraxis_showscale=False # 오른쪽 색상 스케일 바 숨김
    )
    
    # 텍스트 위치 조정
    fig.update_traces(textposition='outside')
    
    return fig

# --- Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(page_title="지역별 범죄 분석", layout="wide")
    st.title("범죄 데이터 분석: 지역별 범죄 비율 시각화")
    st.markdown("---")

    # 1. 데이터 로드
    st.subheader("1. 데이터 파일 업로드")
    uploaded_file = st.file_uploader(
        "분석할 CSV 파일을 업로드해주세요. (crime.csv)", 
        type=['csv'], 
        key="crime_data_uploader"
    )

    df = None
    if uploaded_file is not None:
        try:
            # 인코딩 문제 해결을 위해 'cp949' 또는 'euc-kr' 시도
            uploaded_file.seek(0)
            file_contents = uploaded_file.read()
            
            # UTF-8로 시도
            try:
                df = pd.read_csv(io.StringIO(file_contents.decode('utf-8')))
            except UnicodeDecodeError:
                # UTF-8 실패 시 CP949로 시도
                df = pd.read_csv(io.StringIO(file_contents.decode('cp949')))

            st.success("파일 로드 성공!")
            
            # 데이터 미리보기
            st.subheader("업로드된 데이터 미리보기 (상위 5개 행)")
            st.dataframe(df.head())

            st.markdown("---")

            # 2. 시각화
            st.subheader("2. Plotly 인터랙티브 지역별 범죄 비율 막대 그래프")
            
            # Plotly 그래프 생성 및 표시
            fig = create_crime_ratio_bar_chart(df)
            st.plotly_chart(fig, use_container_width=True)
            
            # 3. Top 5 지역 목록 표시
            df_ranked_display = df.drop(columns=['범죄대분류', '범죄중분류'], errors='ignore').sum().reset_index()
            df_ranked_display.columns = ['지역명', '범죄총합']
            df_ranked_display = df_ranked_display.sort_values(by='범죄총합', ascending=False).head(5).reset_index(drop=True)
            df_ranked_display.index += 1
            
            st.markdown("### 🥇 범죄 발생 총합 Top 5 지역")
            st.table(df_ranked_display)


        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
            st.warning("CSV 파일 형식과 인코딩(UTF-8 또는 CP949)을 확인해 주세요.")

    else:
        st.info("시작하려면 CSV 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
