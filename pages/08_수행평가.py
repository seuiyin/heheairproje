
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="시대별 인기 음악 분석",
    page_icon="🎧",
    layout="wide"
)

st.title("🎧 시대별 인기 음악 분석")
st.write("음악 데이터를 통해 시대에 따른 인기 음악의 변화를 알아보자!")

# CSV 파일 경로
FILE_PATH = Path(__file__).resolve().parent.parent / "music.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(FILE_PATH, encoding="utf-8-sig")
except FileNotFoundError:
    st.error("music.csv 파일을 찾을 수 없습니다. 상위 폴더에 파일이 있는지 확인해 주세요.")
    st.stop()

# 발매 연도 추출
df["release_year"] = pd.to_numeric(
    df["album_release_date"].astype(str).str.extract(r"(\d{4})")[0],
    errors="coerce"
)

# 숫자 데이터 변환
df["track_popularity"] = pd.to_numeric(
    df["track_popularity"], errors="coerce"
)

# 분석 가능한 데이터만 사용
df = df.dropna(subset=["release_year", "track_popularity"])
df["release_year"] = df["release_year"].astype(int)

# 1950~2026년 데이터
df = df[
    (df["release_year"] >= 1950) &
    (df["release_year"] <= 2026)
]

if df.empty:
    st.error("분석할 수 있는 음악 데이터가 없습니다.")
    st.stop()

# 연도 선택
st.subheader("📅 분석할 기간 선택")

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

year_range = st.slider(
    "발매 연도 범위",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 선택한 기간 데이터
selected_df = df[
    (df["release_year"] >= year_range[0]) &
    (df["release_year"] <= year_range[1])
]

if selected_df.empty:
    st.warning("선택한 기간에 데이터가 없습니다.")
    st.stop()

# 주요 수치
st.subheader("📊 음악 데이터 요약")

col1, col2, col3 = st.columns(3)

col1.metric("분석된 음악 수", f"{len(selected_df):,}곡")
col2.metric(
    "평균 인기도",
    f"{selected_df['track_popularity'].mean():.1f}점"
)
col3.metric(
    "분석 기간",
    f"{year_range[0]}~{year_range[1]}년"
)

# 연도별 분석
yearly = selected_df.groupby("release_year").agg(
    평균인기도=("track_popularity", "mean"),
    발매곡수=("track_name", "count")
).reset_index()

st.divider()

# 연도별 평균 인기도
st.subheader("📈 연도별 평균 음악 인기도")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    yearly["release_year"],
    yearly["평균인기도"],
    marker="o"
)
ax.set_xlabel("Release Year")
ax.set_ylabel("Average Popularity")
ax.set_title("Average Music Popularity by Year")
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close(fig)

# 연도별 발매 곡 수
st.subheader("📊 연도별 발매 곡 수")

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(
    yearly["release_year"],
    yearly["발매곡수"]
)
ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Tracks")
ax.set_title("Number of Released Tracks by Year")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close(fig)

st.divider()

# 인기곡 TOP 10
st.subheader("🏆 선택한 기간의 인기곡 TOP 10")

top10 = selected_df.sort_values(
    by="track_popularity",
    ascending=False
).drop_duplicates(
    subset=["track_name", "artist_name"]
).head(10)

top10_display = top10[
    [
        "track_name",
        "artist_name",
        "release_year",
        "track_popularity"
    ]
].copy()

top10_display.columns = [
    "노래 제목",
    "가수",
    "발매 연도",
    "인기도"
]

st.dataframe(
    top10_display,
    use_container_width=True,
    hide_index=True
)

# 분석 결과
st.divider()
st.subheader("💡 데이터 분석 결과")

best_year = yearly.loc[
    yearly["평균인기도"].idxmax()
]

most_tracks_year = yearly.loc[
    yearly["발매곡수"].idxmax()
]

st.write(
    f"🎵 평균 인기도가 가장 높은 연도는 "
    f"**{int(best_year['release_year'])}년**이며, "
    f"평균 인기도는 **{best_year['평균인기도']:.1f}점**입니다."
)

st.write(
    f"📀 데이터에 기록된 발매 곡이 가장 많은 연도는 "
    f"**{int(most_tracks_year['release_year'])}년**이며, "
    f"총 **{int(most_tracks_year['발매곡수'])}곡**입니다."
)

st.caption("※ 인기도는 첨부된 CSV 파일의 track_popularity 값을 기준으로 합니다.")
st.caption("※ 이 데이터는 전체 음악 시장을 대표하는 통계가 아닐 수 있습니다.")
