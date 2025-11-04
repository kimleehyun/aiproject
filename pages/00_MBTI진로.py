import streamlit as st

# 🎨 제목
st.title("✨ MBTI로 보는 나의 진로 추천 ✨")
st.write("MBTI를 선택하면 너에게 어울리는 진로 2가지를 알려줄게 😄")

# 💭 MBTI 목록
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 🎯 MBTI 선택
selected_mbti = st.selectbox("너의 MBTI를 골라봐 👇", mbti_list)

# 💡 MBTI별 진로 추천 데이터
career_dict = {
    "INTJ": ["데이터 분석가 📊", "전략 기획자 🧠"],
    "INTP": ["연구원 🔬", "개발자 💻"],
    "ENTJ": ["CEO 💼", "경영 컨설턴트 📈"],
    "ENTP": ["창업가 🚀", "마케팅 기획자 🎯"],
    "INFJ": ["상담사 💬", "작가 ✍️"],
    "INFP": ["예술가 🎨", "심리상담가 🧘‍♀️"],
    "ENFJ": ["교사 👩‍🏫", "인사담당자 🧑‍💼"],
    "ENFP": ["크리에이터 🎥", "광고기획자 📢"],
    "ISTJ": ["공무원 🏛️", "회계사 📚"],
    "ISFJ": ["간호사 🏥", "사회복지사 💖"],
    "ESTJ": ["관리자 🧱", "군인 🎖️"],
    "ESFJ": ["유치원 교사 🧒", "서비스 매니저 ☕"],
    "ISTP": ["기계 엔지니어 ⚙️", "드론 조종사 🚁"],
    "ISFP": ["패션 디자이너 👗", "사진작가 📸"],
    "ESTP": ["영업사원 💬", "이벤트 플래너 🎉"],
    "ESFP": ["배우 🎭", "MC 🎤"]
}

# 🎁 버튼 클릭 시 결과 보여주기
if st.button("내 진로 보기 💫"):
    careers = career_dict.get(selected_mbti, ["직업 데이터 없음", "직업 데이터 없음"])
    st.subheader(f"👉 {selected_mbti} 타입에게 어울리는 진로는?")
    st.success(f"1️⃣ {careers[0]}\n\n2️⃣ {careers[1]}")
    st.write("너의 성향을 잘 살려서 도전해봐! 💪")

# ✨ 푸터
st.markdown("---")
st.caption("Made with 💙 by ChatGPT + Streamlit")
