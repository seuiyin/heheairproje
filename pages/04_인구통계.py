
import re
from pathlib import Path
from io import BytesIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

PINK = "#FF1493"


# ==========================================
# 2. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_population(uploaded_file=None):

    encodings = ["cp949", "euc-kr", "utf-8-sig", "utf-8"]

    # 사용자가 직접 CSV를 업로드한 경우
    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        for encoding in encodings:
            try:
                return pd.read_csv(
                    BytesIO(file_bytes),
                    encoding=encoding
                )
            except UnicodeDecodeError:
                continue

        raise ValueError("CSV 인코딩을 확인해 주세요.")

    # ★ 핵심 수정 부분 ★
    # page 폴더의 상위 폴더에서 CSV 파일 찾기
    csv_path = Path(__file__).resolve().parent.parent / "population.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV 파일을 찾을 수 없습니다: {csv_path}"
        )

    for encoding in encodings:
        try:
            return pd.read_csv(
                csv_path,
                encoding=encoding
            )
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일의 인코딩을 읽을 수 없습니다.")


# ==========================================
# 3. 화면 제목
# ==========================================

st.title("📊 서울시 연령별 인구 분석")
st.write(
    "행정구역, 성별, 연도를 선택하여 "
    "연령별 인구 분포를 확인해 보세요!"
)


# ==========================================
# 4. 데이터 불러오기
# ==========================================

with st.sidebar:

    st.header("🔎 분석 조건")

    uploaded_csv = st.file_uploader(
        "CSV 파일 업로드 (선택사항)",
        type=["csv"]
    )

try:

    df = load_population(uploaded_csv)

except Exception as error:

    st.error(f"데이터를 불러오지 못했습니다: {error}")
    st.stop()


# ==========================================
# 5. 데이터 전처리
# ==========================================

if "행정구역" not in df.columns:

    st.error("'행정구역' 열을 찾을 수 없습니다.")
    st.stop()


df["행정구역"] = (
    df["행정구역"]
    .astype(str)
    .str.strip()
)


def clean_region_name(value):

    value = re.sub(
        r"\s*\(\d+\)\s*$",
        "",
        value
    ).strip()

    if value.startswith("서울특별시 "):

        value = value.replace(
            "서울특별시 ",
            "",
            1
        ).strip()

    return value


df["지역명"] = df["행정구역"].apply(
    clean_region_name
)


# ==========================================
# 6. 연도 추출
# ==========================================

years = sorted({

    int(match.group(1))

    for column in df.columns

    if (
        match := re.match(
            r"^(\d{4})년_",
            str(column)
        )
    )

})


if not years:

    st.error("연도 데이터를 찾을 수 없습니다.")
    st.stop()


# ==========================================
# 7. 행정구역 목록
# ==========================================

regions = df["지역명"].dropna().unique().tolist()

regions = sorted(
    regions,
    key=lambda x: (x != "서울특별시", x)
)


# ==========================================
# 8. 사용자 선택
# ==========================================

with st.sidebar:

    st.subheader("📍 분석할 지역")

    selected_region = st.selectbox(
        "행정구역 선택",
        regions
    )

    st.subheader("👥 성별")

    selected_gender = st.selectbox(
        "성별 선택",
        ["전체", "남성", "여성"]
    )

    st.subheader("📅 연도")

    selected_year = st.selectbox(
        "연도 선택",
        years,
        index=len(years) - 1
    )


# ==========================================
# 9. 성별 데이터 연결
# ==========================================

gender_prefix = {

    "전체": "",
    "남성": "남_",
    "여성": "여_"

}[selected_gender]


selected_data = df[
    df["지역명"] == selected_region
]


if selected_data.empty:

    st.error("선택한 지역의 데이터가 없습니다.")
    st.stop()


selected_data = selected_data.iloc[0]


# ==========================================
# 10. 연령별 인구 데이터 추출
# ==========================================

age_labels = []
age_midpoints = []
population_values = []


prefix = (
    f"{selected_year}년_"
    f"{gender_prefix}거주자_"
)


for column in df.columns:

    column = str(column)

    if not column.startswith(prefix):
        continue

    age_part = column[len(prefix):]

    # 5세 단위 연령
    match = re.fullmatch(
        r"(\d+)~(\d+)세",
        age_part
    )

    if match:

        start_age = int(match.group(1))
        end_age = int(match.group(2))

        age_labels.append(
            f"{start_age}~{end_age}세"
        )

        age_midpoints.append(
            (start_age + end_age) / 2
        )

        population_values.append(
            pd.to_numeric(
                selected_data[column],
                errors="coerce"
            )
        )

        continue

    # 100세 이상
    open_match = re.fullmatch(
        r"(\d+)세 이상",
        age_part
    )

    if open_match:

        start_age = int(open_match.group(1))

        age_labels.append(
            f"{start_age}세 이상"
        )

        age_midpoints.append(start_age)

        population_values.append(
            pd.to_numeric(
                selected_data[column],
                errors="coerce"
            )
        )


if not age_labels:

    st.error("연령별 인구 데이터를 찾을 수 없습니다.")
    st.stop()


# ==========================================
# 11. 그래프 데이터 정리
# ==========================================

chart_df = pd.DataFrame({

    "연령대": age_labels,
    "나이": age_midpoints,
    "인구수": population_values

})


chart_df = chart_df.dropna(
    subset=["인구수"]
)

chart_df["인구수"] = (
    chart_df["인구수"].astype(float)
)


# ==========================================
# 12. 인구 정보 표시
# ==========================================

total_population = int(
    chart_df["인구수"].sum()
)


col1, col2, col3 = st.columns(3)


col1.metric(
    "📍 선택 지역",
    selected_region
)


col2.metric(
    "👥 선택 성별",
    selected_gender
)


col3.metric(
    "🏙️ 연령별 인구 합계",
    f"{total_population:,}명"
)


st.divider()


# ==========================================
# 13. 꺾은선 그래프
# ==========================================

st.subheader("📈 연령별 인구 분포")


fig = go.Figure()


fig.add_trace(

    go.Scatter(

        x=chart_df["나이"],

        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color=PINK,
            width=3
        ),

        marker=dict(
            color=PINK,
            size=7
        ),

        customdata=chart_df[
            ["연령대"]
        ].to_numpy(),

        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "인구수: %{y:,.0f}명"
            "<extra></extra>"
        )

    )

)


# ==========================================
# 14. 가로축 10세 단위 눈금
# ==========================================

tick_positions = list(
    range(0, len(chart_df), 2)
)


tick_values = (
    chart_df["나이"]
    .iloc[tick_positions]
    .tolist()
)


tick_text = (
    chart_df["연령대"]
    .iloc[tick_positions]
    .tolist()
)


# 마지막 연령대 표시
if chart_df["연령대"].iloc[-1].endswith("이상"):

    tick_values.append(
        chart_df["나이"].iloc[-1]
    )

    tick_text.append(
        chart_df["연령대"].iloc[-1]
    )


# 중복 눈금 제거
unique_ticks = {}

for value, label in zip(
    tick_values,
    tick_text
):

    unique_ticks[value] = label


# ==========================================
# 15. 세로축 1000명 단위 눈금
# ==========================================

max_population = float(
    chart_df["인구수"].max()
)


y_max = max(
    1000,
    ((int(max_population) // 1000) + 1) * 1000
)


# ==========================================
# 16. 그래프 디자인
# ==========================================

fig.update_layout(

    title=dict(

        text=(
            f"{selected_region} "
            f"{selected_year}년 "
            f"{selected_gender} 연령별 인구"
        ),

        x=0.5,
        xanchor="center"

    ),

    xaxis=dict(

        title="나이",

        tickmode="array",

        tickvals=list(
            unique_ticks.keys()
        ),

        ticktext=list(
            unique_ticks.values()
        ),

        showgrid=True,

        gridcolor="#E8E8E8",

        zeroline=False

    ),

    yaxis=dict(

        title="인구수 (명)",

        range=[0, y_max],

        dtick=1000,

        tickformat=",",

        showgrid=True,

        gridcolor="#E8E8E8",

        zeroline=False

    ),

    plot_bgcolor="white",

    paper_bgcolor="white",

    hovermode="x unified",

    margin=dict(
        l=25,
        r=25,
        t=75,
        b=45
    ),

    font=dict(
        family="Malgun Gothic, Apple SD Gothic Neo, sans-serif"
    )

)


# ==========================================
# 17. 그래프 출력
# ==========================================

st.plotly_chart(
    fig,
    use_container_width=True
)


st.caption(
    "※ 원본 데이터는 5세 단위로 구성되어 있습니다. "
    "가로축 주요 눈금은 10세 간격이며, "
    "세로축 눈금은 1,000명 간격입니다."
)


# ==========================================
# 18. 상세 데이터 확인
# ==========================================

with st.expander("📋 연령별 인구 데이터 확인"):

    display_df = chart_df[
        ["연령대", "인구수"]
    ].copy()

    display_df["인구수"] = (
        display_df["인구수"]
        .round(0)
        .astype("int64")
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.success("🎉 인구 통계 분석이 완료되었습니다!")
