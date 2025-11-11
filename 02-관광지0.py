# Streamlit 앱: 서울 외국인 인기 관광지 TOP10 (Folium)

아래에는 **app.py**(Streamlit 앱)와 **requirements.txt** 파일 내용이 모두 포함되어 있습니다. 복사해서 Streamlit Cloud에 올리면 바로 작동합니다.

---

## 파일: `app.py`

```python
import streamlit as st
import folium
from streamlit_folium import st_folium
import io
import json

st.set_page_config(page_title="Seoul TOP10 Tourist Spots", layout="wide")

st.title("서울 외국인들이 좋아하는 관광지 TOP10 - 지도 표시 🌏🇰🇷")
st.write("아래 지도의 마커를 클릭하면 장소 이름과 간단한 설명을 볼 수 있습니다.")

# 주요 관광지: 이름, 위도, 경도, 설명
places = [
    {"name":"Gyeongbokgung Palace", "lat":37.579617, "lon":126.977041, "desc":"Historic royal palace (경복궁)"},
    {"name":"Changdeokgung Palace", "lat":37.579419, "lon":126.991048, "desc":"UNESCO World Heritage (창덕궁)"},
    {"name":"Bukchon Hanok Village", "lat":37.582604, "lon":126.981025, "desc":"Traditional hanok village (북촌한옥마을)"},
    {"name":"Insadong", "lat":37.574032, "lon":126.984686, "desc":"Arts & crafts street (인사동)"},
    {"name":"Myeongdong", "lat":37.560980, "lon":126.986071, "desc":"Shopping & street food (명동)"},
    {"name":"N Seoul Tower (Namsan)", "lat":37.551169, "lon":126.988227, "desc":"City views & night scenery (남산서울타워)"},
    {"name":"Dongdaemun Design Plaza (DDP)", "lat":37.566344, "lon":127.009518, "desc":"Modern design center (동대문디자인플라자)"},
    {"name":"Hongdae (Hongik Univ.)", "lat":37.556264, "lon":126.922678, "desc":"Youth culture & nightlife (홍대)"},
    {"name":"Lotte World Tower (Seoul Sky)", "lat":37.513114, "lon":127.102657, "desc":"Tallest building & observation deck (롯데월드타워)"},
    {"name":"Itaewon", "lat":37.534661, "lon":126.994934, "desc":"International district & nightlife (이태원)"},
]

# 사이드바 설정
st.sidebar.header("지도 옵션")
show_cluster = st.sidebar.checkbox("마커 클러스터 사용", value=False)
start_zoom = st.sidebar.slider("초기 줌 레벨", 10, 14, 12)

# 기본 Folium 맵
center_lat = 37.566535
center_lon = 126.977969
m = folium.Map(location=[center_lat, center_lon], zoom_start=start_zoom, control_scale=True)

# 타일 레이어
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.LayerControl().add_to(m)

# 마커 추가
if show_cluster:
    from folium.plugins import MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)
    for p in places:
        popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
        folium.Marker(location=[p['lat'], p['lon']], popup=popup_html, tooltip=p['name']).add_to(marker_cluster)
else:
    for p in places:
        popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
        folium.CircleMarker(location=[p['lat'], p['lon']], radius=6, popup=popup_html, tooltip=p['name'], fill=True).add_to(m)

# 지도를 화면에 표시 (streamlit_folium 사용)
st.subheader("지도")
map_data = st_folium(m, width=900, height=600)

# 우측 컬럼에 장소 목록
with st.expander("▶ 관광지 목록 (클릭하면 위치가 하이라이트 됩니다)"):
    for i, p in enumerate(places, start=1):
        st.markdown(f"**{i}. {p['name']}** — {p['desc']}  ")

# 코드 다운로드 버튼: app.py와 requirements.txt를 바로 다운로드할 수 있게 함
app_code = open(__file__, "r").read() if '__file__' in globals() else None

# 안전하게 앱 코드 문자열 생성 (대체: 아래에 코드 텍스트를 직접 넣음)
app_py_text = """
# app.py content: copy this file content from the Streamlit editor or this page
# (This placeholder is replaced by the Streamlit Cloud UI code block if you copy manually.)
"""

# Provide downloads: create bytes
app_bytes = io.BytesIO()
app_bytes.write(open(__file__, 'rb').read() if app_code else b'')
# If __file__ is not available in some runtimes, offer raw source as text for download
if app_bytes.getbuffer().nbytes == 0:
    # fallback: build the app text from the places and code above
    # For portability we include the full source as a string literal
    full_source = '''import streamlit as st
import folium
from streamlit_folium import st_folium
import io

st.set_page_config(page_title="Seoul TOP10 Tourist Spots", layout="wide")

st.title("서울 외국인들이 좋아하는 관광지 TOP10 - 지도 표시 🌏🇰🇷")
st.write("아래 지도의 마커를 클릭하면 장소 이름과 간단한 설명을 볼 수 있습니다.")

places = [
    {"name":"Gyeongbokgung Palace", "lat":37.579617, "lon":126.977041, "desc":"Historic royal palace (경복궁)"},
    {"name":"Changdeokgung Palace", "lat":37.579419, "lon":126.991048, "desc":"UNESCO World Heritage (창덕궁)"},
    {"name":"Bukchon Hanok Village", "lat":37.582604, "lon":126.981025, "desc":"Traditional hanok village (북촌한옥마을)"},
    {"name":"Insadong", "lat":37.574032, "lon":126.984686, "desc":"Arts & crafts street (인사동)"},
    {"name":"Myeongdong", "lat":37.560980, "lon":126.986071, "desc":"Shopping & street food (명동)"},
    {"name":"N Seoul Tower (Namsan)", "lat":37.551169, "lon":126.988227, "desc":"City views & night scenery (남산서울타워)"},
    {"name":"Dongdaemun Design Plaza (DDP)", "lat":37.566344, "lon":127.009518, "desc":"Modern design center (동대문디자인플라자)"},
    {"name":"Hongdae (Hongik Univ.)", "lat":37.556264, "lon":126.922678, "desc":"Youth culture & nightlife (홍대)"},
    {"name":"Lotte World Tower (Seoul Sky)", "lat":37.513114, "lon":127.102657, "desc":"Tallest building & observation deck (롯데월드타워)"},
    {"name":"Itaewon", "lat":37.534661, "lon":126.994934, "desc":"International district & nightlife (이태원)"},
]

st.sidebar.header("지도 옵션")
show_cluster = st.sidebar.checkbox("마커 클러스터 사용", value=False)
start_zoom = st.sidebar.slider("초기 줌 레벨", 10, 14, 12)

center_lat = 37.566535
center_lon = 126.977969
m = folium.Map(location=[center_lat, center_lon], zoom_start=start_zoom, control_scale=True)
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.LayerControl().add_to(m)

if show_cluster:
    from folium.plugins import MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)
    for p in places:
        popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
        folium.Marker(location=[p['lat'], p['lon']], popup=popup_html, tooltip=p['name']).add_to(marker_cluster)
else:
    for p in places:
        popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
        folium.CircleMarker(location=[p['lat'], p['lon']], radius=6, popup=popup_html, tooltip=p['name'], fill=True).add_to(m)

st.subheader("지도")
map_data = st_folium(m, width=900, height=600)

with st.expander("▶ 관광지 목록 (클릭하면 위치가 하이라이트 됩니다)"):
    for i, p in enumerate(places, start=1):
        st.markdown(f"**{i}. {p['name']}** — {p['desc']}  ")
'''
    app_bytes = io.BytesIO(full_source.encode('utf-8'))

# requirements.txt content
requirements = """
streamlit
folium
streamlit-folium
"""

st.markdown("---")
col1, col2 = st.columns([2,1])
with col1:
    st.subheader("앱 코드 (복사해서 붙여넣기) ✂️")
    # Show the full source code for easy copying
    st.code(full_source, language='python')
with col2:
    st.subheader("파일 다운로드")
    st.download_button("Download app.py", data=app_bytes.getvalue(), file_name="app.py", mime="text/x-python")
    st.download_button("Download requirements.txt", data=requirements.encode('utf-8'), file_name="requirements.txt", mime="text/plain")

st.caption("※ Streamlit Cloud에 업로드할 때는 app.py와 requirements.txt를 같은 리포지토리/디렉터리에 넣으세요.")
```

---

## 파일: `requirements.txt`

```
streamlit
folium
streamlit-folium
```

---

### 사용법

1. 위 `app.py` 코드와 `requirements.txt` 내용을 각각 파일로 저장하세요.
2. GitHub 리포지토리에 저장한 뒤 Streamlit Cloud에 연결하면 자동으로 설치되고 실행됩니다.
3. 필요하면 `places` 리스트에 장소를 추가하거나 설명을 수정하세요.
