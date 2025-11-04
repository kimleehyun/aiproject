import streamlit as st

# MBTI 유형과 추천 도서 및 영화 데이터
recommendations = {
    "INTJ": {
        "books": ["'생각의 지도' by 조승연", "'디자인 사고' by Tim Brown"],
        "movies": ["Inception", "Interstellar"],
        "reasons": ["INTJ는 창의적이고 미래 지향적인 사고를 좋아해요. '생각의 지도'와 '디자인 사고'는 그들의 문제 해결 능력과 창의력에 도움을 줄 수 있어요. 영화는 복잡한 이야기와 깊이 있는 스토리를 좋아하는 성향에 맞춰 선택했어요."]
    },
    "INFP": {
        "books": ["'어린 왕자' by 앙투안 드 생텍쥐페리", "'고양이를 부탁해' by 김호연"],
        "movies": ["The Secret Life of Walter Mitty", "The Perks of Being a Wallflower"],
        "reasons": ["INFP는 감성적이고 상상력이 풍부해요. '어린 왕자'는 감성적이고 철학적인 메시지가 있어요. 영화는 삶의 의미를 찾는 여정을 그린 작품으로 INFP에게 잘 맞아요."]
    },
    # 추가적인 MBTI 유형을 여기에 추가할 수 있습니다.
}

# 앱 제목
st.title('MBTI 유형에 따른 책과 영화 추천 🎬📚')

# MBTI 유형 선택
mbti_type = st.selectbox("당신의 MBTI 유형을 선택하세요!", ["INTJ", "INFP", "ENTP", "ISFJ", "ESTP", "INFJ", "ESFP", "ISTJ", "INTP", "ENFP", "ISTP", "ISFP", "ENTJ", "ESFJ", "ESTJ", "ISFJ"])

# 추천 책, 영화, 이유 보여주기
if mbti_type in recommendations:
    st.subheader(f"{mbti_type}에 대한 추천 👇")
    st.write("**추천 도서**:")
    for book in recommendations[mbti_type]["books"]:
        st.write(f"- {book}")

    st.write("**추천 영화**:")
    for movie in recommendations[mbti_type]["movies"]:
        st.write(f"- {movie}")

    st.write("**추천 이유**:")
    st.write(recommendations[mbti_type]["reasons"][0])

