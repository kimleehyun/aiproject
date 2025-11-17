# app.py (수정본)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Subway Top10 (Oct 2025)", layout="wide")
st.title("지하철 승하차 Top10 — 2025년 10월 한 날 선택")
st.caption("파일 업로드하거나 리포지토리 내 'subway.csv'를 사용하세요.")

#
# 파일 로드 (업로드 우선, 없으면 로컬 경로 시도)
#
uploaded = st.file_uploader("CSV 파일 업로드 (UTF-8/CP949 가능)", type=["csv"])
df = None
used_encoding = None

def try_read_file(filelike):
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr', 'latin1']
    last_err = None
    for enc in encodings:
        try:
            filelike.seek(0)
            return pd.read_csv(filelike, encoding=enc), enc
        except Exception as e:
            last_err = e
    raise last_err

try:
    if uploaded is not None:
        df, used_encoding = try_read_file(uploaded)
    else:
        # 로컬 시도: 여러 인코딩으로
        try:
            df = pd.read_csv("subway.csv", encoding='cp949')
            used_encoding = 'cp949'
        except Exception:
            try:
                df = pd.read_csv("subway.csv", encoding='utf-8')
                used_encoding = 'utf-8'
            except Exception as e:
                st.warning("업로드된 파일이 없고 로컬 'subway.csv'도 읽을 수 없습니다. 먼저 업로드해주세요.")
                st.stop()
except Exception as e:
    st.error(f"파일을 읽는 도중 에러가 발생했습니다: {e}")
    st.stop()

st.sidebar.markdown(f"**읽은 파일 인코딩 추정:** `{used_encoding}`")
st.write("파일 미리보기 (상위 10행)")
st.dataframe(df.head(10), use_container_width=True)

#
# 유연한 컬럼 자동 탐지
#
def find_column(candidates, cols):
    if cols is None:
        return None
    # 완전 일치
    for c in candidates:
        for col in cols:
            if col.strip().lower() == c.strip().lower():
                return col
    # 공백/밑줄/소문자 정규화 후 비교
    norm = {col: col.strip().lower().replace(" ", "").replace("_","") for col in cols}
    for c in candidates:
        key = c.strip().lower().replace(" ", "").replace("_","")
        for orig, n in norm.items():
            if key == n:
                return orig
    # 부분일치 허용 (단, 너무 짧은 후보는 제외)
    for c in candidates:
        if len(c) < 3:
            continue
        for col in cols:
            if c.strip().lower() in col.strip().lower() or col.strip().lower() in c.
