import streamlit as st
import pydeck as pdk

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울 외국인 관광객 TOP 10",
    page_icon="📍",
    layout="wide"
)

# -----------------------------
# 관광지 데이터
# -----------------------------
places = [
    {
        "rank": 1,
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9826,
        "description": "쇼핑, K-뷰티, 길거리 음식 등을 한곳에서 즐길 수 있는 서울 대표 관광거리예요."
    },
    {
        "rank": 2,
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.5669,
        "lon": 127.0098,
        "description": "독특한 건축물과 디자인 전시, 패션 문화를 경험할 수 있는 서울의 랜드마크예요."
    },
    {
        "rank": 3,
        "name": "남산서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "서울 시내를 한눈에 내려다볼 수 있는 전망 명소로 서울의 대표적인 상징 중 하나예요."
    },
    {
        "rank": 4,
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선시대 대표 궁궐로, 한국의 전통 건축과 역사를 가까이에서 볼 수 있어요."
    },
    {
        "rank": 5,
        "name": "홍대거리",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리 공연, 카페, 쇼핑과 젊은 문화를 즐길 수 있어 외국인 관광객에게도 인기 있는 곳이에요."
    },
    {
        "rank": 6,
        "name": "남대문시장",
        "lat": 37.5591,
        "lon": 126.9775,
        "description": "오랜 역사를 가진 전통시장으로 다양한 먹거리와 쇼핑을 즐길 수 있어요."
    },
    {
        "rank": 7,
        "name": "인사동",
        "lat": 37.5740,
        "lon": 126.9855,
        "description": "전통 공예품과 기념품, 전통적인 분위기의 가게가 많아 한국 문화를 체험하기 좋아요."
    },
    {
        "rank": 8,
        "name": "강남역",
        "lat": 37.4979,
        "lon": 127.0276,
        "description": "쇼핑과 맛집, 카페, 엔터테인먼트가 모여 있는 현대적인 서울의 중심 상권이에요."
    },
    {
        "rank": 9,
        "name": "국립중앙박물관",
        "lat": 37.5239,
        "lon": 126.9804,
        "description": "한국의 역사와 문화유산을 다양한 전시를 통해 살펴볼 수 있는 대표 박물관이에요."
    },
    {
        "rank": 10,
        "name": "잠실·롯데월드",
        "lat": 37.5111,
        "lon": 127.0980,
        "description": "테마파크와 쇼핑, 전망대 등을 함께 즐길 수 있어 가족·친구 여행지로 인기가 높아요."
    },
]

# -----------------------------
# 제목
# -----------------------------
st.title("🇰🇷 서울 외국인 관광객 추천 TOP 10")

st.caption(
    "서울을 처음 방문하는 외국인 여행자들이 많이 찾는 "
    "대표 관광지를 한눈에 확인해 보세요! ✈️"
)

# -----------------------------
# 지도 설정
# -----------------------------
layer = pdk.Layer(
    "ScatterplotLayer",
    data=places,

    # 위치
    get_position="[lon, lat]",

    # 마커 크기
    get_radius=550,

    # 마커 색상
    get_fill_color=[220, 70, 70, 190],

    # 마커 테두리
    get_line_color=[255, 255, 255, 220],

    line_width_min_pixels=2,

    # 마우스를 올렸을 때 정보 표시
    pickable=True,
)

# 서울 중심으로 지도 위치 설정
view_state = pdk.ViewState(
    latitude=37.55,
    longitude=126.99,
    zoom=10.8,
    pitch=0,
)

# 마커에 마우스를 올렸을 때 나타나는 설명
tooltip = {
    "html": """
        <b>#{rank} {name}</b>
        <br/>
        {description}
    """,
    "style": {
        "backgroundColor": "white",
        "color": "black",
        "fontSize": "14px",
        "padding": "8px"
    }
}

# 지도 생성
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="light"
)

# -----------------------------
# 지도 화면 출력
# -----------------------------
st.pydeck_chart(
    deck,
    use_container_width=True
)

# -----------------------------
# 관광지 설명
# -----------------------------
st.subheader("📌 관광지 간단 설명")

for place in places:

    st.markdown(
        f"""
        **{place['rank']}. {place['name']}**

        {place['description']}
        """
    )

# -----------------------------
# 안내 문구
# -----------------------------
st.divider()

st.caption(
    "※ TOP 10은 서울시 공식 관광정보에서 외국인 관광객에게 "
    "대표적으로 소개되는 관광지와 서울시 관광객 방문 통계 자료를 "
    "참고해 교육용으로 구성했습니다. "
    "순위는 실시간 공식 순위를 의미하지 않습니다."
)
