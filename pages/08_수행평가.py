
import streamlit as st
import random

st.set_page_config(
    page_title="World Music Trip 🌎",
    page_icon="🎧",
    layout="centered"
)

# -------------------------------
# 🌎 국가 목록 (159개)
# -------------------------------

countries = """
가나
가봉
가이아나
감비아
과테말라
그레나다
그리스
기니
기니비사우
나미비아
나우루
나이지리아
남아프리카공화국
남수단
네덜란드
네팔
노르웨이
뉴질랜드
니제르
니카라과
대한민국
덴마크
도미니카공화국
독일
라오스
라이베리아
라트비아
러시아
레바논
레소토
루마니아
룩셈부르크
르완다
리투아니아
마다가스카르
말라위
말레이시아
말리
멕시코
모나코
모로코
모리셔스
모리타니
모잠비크
몬테네그로
몰도바
몰디브
몽골
미국
미얀마
바누아투
바레인
바베이도스
바하마
방글라데시
베냉
베네수엘라
베트남
벨기에
벨리즈
보스니아 헤르체고비나
보츠와나
볼리비아
부룬디
부르키나파소
부탄
북마케도니아
불가리아
브라질
브루나이
사모아
사우디아라비아
산마리노
상투메 프린시페
세네갈
세르비아
세이셸
세인트루시아
소말리아
솔로몬제도
수단
수리남
스리랑카
스웨덴
스위스
스페인
슬로바키아
슬로베니아
시리아
시에라리온
싱가포르
아랍에미리트
아르메니아
아르헨티나
아이슬란드
아이티
아일랜드
아제르바이잔
아프가니스탄
안도라
알바니아
알제리
앙골라
앤티가 바부다
에리트레아
에스토니아
에콰도르
에티오피아
엘살바도르
영국
예멘
오만
오스트레일리아
오스트리아
온두라스
요르단
우간다
우루과이
우즈베키스탄
우크라이나
이라크
이란
이스라엘
이집트
이탈리아
인도
인도네시아
일본
자메이카
잠비아
적도기니
조지아
중국
중앙아프리카공화국
지부티
짐바브웨
차드
체코
칠레
카메룬
카자흐스탄
카타르
캄보디아
캐나다
케냐
코모로
코스타리카
코트디부아르
콜롬비아
콩고
콩고민주공화국
쿠바
쿠웨이트
크로아티아
키르기스스탄
키리바시
키프로스
타지키스탄
탄자니아
태국
토고
통가
튀니지
튀르키예
파나마
파라과이
파키스탄
파푸아뉴기니
페루
포르투갈
폴란드
프랑스
핀란드
필리핀
헝가리
""".strip().split("\n")

# -------------------------------
# 🎵 국가별 노래 데이터
# 형식: 제목, 가수, 발매 연도
# -------------------------------

music_data = {
    "대한민국": [
        ("Gee", "소녀시대", 2009),
        ("Dynamite", "방탄소년단", 2020),
        ("좋은 날", "아이유", 2010)
    ],
    "일본": [
        ("Lemon", "요네즈 켄시", 2018),
        ("First Love", "우타다 히카루", 1999),
        ("Pretender", "Official髭男dism", 2019)
    ],
    "미국": [
        ("Billie Jean", "Michael Jackson", 1982),
        ("Like a Rolling Stone", "Bob Dylan", 1965),
        ("Blinding Lights", "The Weeknd", 2019)
    ],
    "영국": [
        ("Bohemian Rhapsody", "Queen", 1975),
        ("Yesterday", "The Beatles", 1965),
        ("Shape of You", "Ed Sheeran", 2017)
    ],
    "프랑스": [
        ("Alors on danse", "Stromae", 2009),
        ("Dernière danse", "Indila", 2013),
        ("Joe le taxi", "Vanessa Paradis", 1987)
    ],
    "캐나다": [
        ("My Heart Will Go On", "Celine Dion", 1997),
        ("Sorry", "Justin Bieber", 2015),
        ("Call Me Maybe", "Carly Rae Jepsen", 2011)
    ],
    "독일": [
        ("99 Luftballons", "Nena", 1983),
        ("Du hast", "Rammstein", 1997),
        ("Atemlos durch die Nacht", "Helene Fischer", 2013)
    ],
    "이탈리아": [
        ("Nel blu dipinto di blu", "Domenico Modugno", 1958),
        ("L'italiano", "Toto Cutugno", 1983),
        ("Zitti e buoni", "Måneskin", 2021)
    ],
    "스웨덴": [
        ("Dancing Queen", "ABBA", 1976),
        ("The Sign", "Ace of Base", 1993),
        ("Wake Me Up", "Avicii", 2013)
    ],
    "브라질": [
        ("Mas, que Nada!", "Jorge Ben Jor", 1963),
        ("Ai Se Eu Te Pego", "Michel Teló", 2011),
        ("Garota de Ipanema", "Tom Jobim", 1962)
    ],
    "인도": [
        ("Jai Ho", "A. R. Rahman", 2008),
        ("Kal Ho Naa Ho", "Sonu Nigam", 2003),
        ("Chaiyya Chaiyya", "Sukhwinder Singh", 1998)
    ],
    "멕시코": [
        ("La Bamba", "Ritchie Valens", 1958),
        ("Eres", "Café Tacvba", 2003),
        ("Limón y Sal", "Julieta Venegas", 2006)
    ],
    "스페인": [
        ("Bailando", "Enrique Iglesias", 2014),
        ("La Macarena", "Los del Río", 1993),
        ("Despacito", "Luis Fonsi", 2017)
    ],
    "호주": [
        ("Down Under", "Men at Work", 1981),
        ("Chandelier", "Sia", 2014),
        ("Somebody That I Used to Know", "Gotye", 2011)
    ],
    "자메이카": [
        ("One Love", "Bob Marley", 1977),
        ("No Woman, No Cry", "Bob Marley & The Wailers", 1974),
        ("Temperature", "Sean Paul", 2005)
    ],
    "아일랜드": [
        ("With or Without You", "U2", 1987),
        ("Zombie", "The Cranberries", 1994),
        ("Nothing Compares 2 U", "Sinéad O'Connor", 1990)
    ],
    "아르헨티나": [
        ("De Música Ligera", "Soda Stereo", 1990),
        ("La Bamba", "Los Fabulosos Cadillacs", 1986),
        ("Persiana Americana", "Soda Stereo", 1986)
    ],
    "필리핀": [
        ("Anak", "Freddie Aguilar", 1978),
        ("Tadhana", "Up Dharma Down", 2012),
        ("Torete", "Moonstar88", 2002)
    ],
    "태국": [
        ("คู่คอง", "ก้อง ห้วยไร่", 2016),
        ("แพ้ทาง", "LABANOON", 2016),
        ("รักติดไซเรน", "ไอซ์ พาริส & แพรวา", 2019)
    ],
    "나이지리아": [
        ("African Queen", "2Baba", 2004),
        ("Ye", "Burna Boy", 2018),
        ("Essence", "Wizkid ft. Tems", 2020)
    ]
}

# -------------------------------
# 🎨 앱 디자인
# -------------------------------

st.title("🌎 World Music Trip")
st.subheader("세계 159개국의 음악 여행 🎧")

st.write(
    "나라를 선택하고 그 나라의 음악을 만나봐! "
    "익숙한 노래부터 새로운 음악까지 함께 탐험해 보자 🌍"
)

st.divider()

st.markdown("### 🎵 어느 나라의 음악이 궁금해?")

country = st.selectbox(
    "국가 선택하기",
    countries,
    index=countries.index("대한민국")
)

# -------------------------------
# 🎼 음악 추천
# -------------------------------

st.divider()

st.markdown(f"## 🎧 {country}의 추천 음악")

if country in music_data:

    songs = music_data[country]

    for i, song in enumerate(songs, 1):

        title, artist, year = song

        with st.container(border=True):

            st.markdown(f"### {['🥇', '🥈', '🥉'][i-1]} {title}")

            st.write(f"🎤 **가수:** {artist}")
            st.write(f"📅 **발매 연도:** {year}년")

            # 유튜브 검색 링크
            import urllib.parse

            query = urllib.parse.quote(
                f"{title} {artist} official audio"
            )

            st.link_button(
                "🎵 노래 검색하기",
                f"https://www.youtube.com/results?search_query={query}"
            )

    st.success("음악 여행 완료! 새로운 노래도 들어봐 🎶")

else:

    st.info(
        "🎵 이 국가의 추천곡 데이터는 아직 준비 중이야!\n\n"
        "잘못된 노래나 가수를 추천하지 않기 위해 "
        "검증된 음악 데이터가 등록된 국가만 보여주고 있어."
    )

    st.caption(
        "앞으로 국가별 음악 데이터를 추가하면 "
        "이곳에서도 3곡씩 추천할 수 있어!"
    )

# -------------------------------
# 🌟 하단 안내
# -------------------------------

st.divider()

st.markdown("### 💡 World Music Tip")

st.write(
    "음악은 언어가 달라도 서로의 문화를 이해하게 해주는 "
    "멋진 방법이야. 오늘은 새로운 나라의 음악에 도전해 봐! 🌏"
)

st.caption(
    "※ 발매 연도는 대표적인 음원 발매 기준이며, "
    "일부 곡은 국가별 최초 발매일과 차이가 있을 수 있어."
)

