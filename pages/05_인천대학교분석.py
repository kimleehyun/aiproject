import streamlit as st
import pandas as pd
import plotly.express as px
import io
import base64

def create_plotly_bar_chart(df_data):
    """
    대학교 데이터를 이용해 순위 비율 막대 그래프를 생성합니다.
    (순위는 임의의 가중치로 계산됩니다.)
    """
    # 1. 대학구분이 '대학'인 학교만 필터링
    df_university = df_data[df_data['대학구분'] == '대학'].copy()
    
    # 2. 임의의 순위 점수 부여 (인터랙티브 시각화를 위한 가상의 순위)
    # 국립대법인: 100점, 국립: 90점, 사립: 70점
    # 본교: +10점, 분교: 0점
    
    def calculate_score(row):
        score = 0
        if row['설립구분'] == '국립대법인':
            score += 100
        elif row['설립구분'] == '국립':
            score += 90
        elif row['설립구분'] == '사립':
            score += 70
        
        if row['본분교'] == '본교':
            score += 10
        
        # 교육대학은 특수 목적으로 간주하여 점수 조정
        if row['학교구분'] == '교육대학':
            score = 95 # 국립대와 비슷한 가중치
        
        # 학교명이 캠퍼스 형태로 분교 표시된 경우 학교명 통일
        school_name = row['학교명']
        if '캠퍼스' in school_name or '국제' in school_name or '메디컬' in school_name:
            # 괄호 안에 있는 내용 제거 (예: 가천대학교 메디컬캠퍼스 -> 가천대학교)
            school_name = school_name.split(' ')[0]
            if school_name.endswith('스'): # '국제캠퍼스'처럼 띄어쓰기 없이 붙은 경우 처리
                 school_name = school_name.replace(' 국제캠퍼스', '').replace(' 메디컬캠퍼스', '')
        
        return score, school_name

    df_university[['점수', '표시_학교명']] = df_university.apply(
        lambda row: pd.Series(calculate_score(row)), axis=1
    )
    
    # 3. 학교별 최고 점수만 선택하여 순위 결정
    # 동일 학교의 캠퍼스가 있는 경우 (ex. 가천대), 최고 점수를 해당 학교의 점수로 사용
    df_ranked = df_university.groupby('표시_학교명')['점수'].max().reset_index()
    df_ranked = df_ranked.sort_values(by='점수', ascending=False).reset_index(drop=True)
    df_ranked['순위'] = df_ranked.index + 1
    
    # 4. 순위 비율 (점수) 계산
    total_score = df_ranked['점수'].sum()
    df_ranked['비율'] = (df_ranked['점수'] / total_score) * 100
    
    # 5. 색상 처리: 1등은 빨간색, 나머지는 그라데이션
    color_map = {}
    
    # 1등 학교 이름
    top_school = df_ranked.iloc[0]['표시_학교명']
    color_map[top_school] = 'red'
    
    # 나머지 학교에 대한 그라데이션 색상 (Plotly 기본 색상 스케일 사용)
    # Plotly Express의 'viridis' 등 내장 스케일을 사용하면 자동으로 그라데이션 적용 가능
    
    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        df_ranked,
        x='표시_학교명',
        y='비율',
        text='순위', # 막대 위에 순위 표시
        color='표시_학교명', # 학교 이름별로 색상 구분
        color_discrete_map=color_map, # 1등 학교 색상 지정
        title='🏫 인천 지역 대학교 순위 비율 (임의 가중치 기반)',
        labels={'표시_학교명': '대학교명', '비율': '순위 비율 (%)'},
        hover_data=['순위', '점수'] # 마우스 오버 시 순위와 점수 표시
    )

    # 1등 학교 막대 색상을 빨간색으로 강제 지정
    colors = ['red' if name == top_school else c for name, c in zip(df_ranked['표시_학교명'], px.colors.sequential.Viridis)]

    fig.update_traces(
        marker_color=colors, # 색상 리스트 적용
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'}, # 비율(y축 값)에 따라 내림차순 정렬
        yaxis_title='순위 비율 (%)',
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        showlegend=False # 범례 숨김 (막대 색상으로 학교명 구분이 충분함)
    )
    
    return fig

# --- Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(page_title="인천 대학교 분석", layout="wide")
    st.title("인천 지역 대학교 순위 및 시각화")
    st.markdown("---")

    # 1. 데이터 로드
    # 사용자가 파일을 업로드하도록 유도 (Streamlit Cloud 환경에서 작동)
    st.subheader("1. 데이터 파일 업로드")
    uploaded_file = st.file_uploader(
        "분석할 CSV 파일을 업로드해주세요.", 
        type=['csv'], 
        key="university_data_uploader"
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
            st.subheader("업로드된 데이터 미리보기")
            st.dataframe(df.head())

            st.markdown("---")

            # 2. 시각화
            st.subheader("2. Plotly 인터랙티브 순위 비율 막대 그래프")
            
            # Plotly 그래프 생성 및 표시
            fig = create_plotly_bar_chart(df)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(
                """
                > **참고:** 순위는 데이터의 **설립구분** (국립대법인 > 국립 > 사립)과 **본분교** (본교 > 분교)에 
                > 임의의 가중치를 부여하여 계산된 **가상의 순위**입니다. 실제 대학교 평가 순위가 아님에 유의해 주세요.
                """
            )

        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
            st.warning("CSV 파일 형식과 인코딩(UTF-8 또는 CP949)을 확인해 주세요.")

    else:
        st.info("시작하려면 CSV 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
