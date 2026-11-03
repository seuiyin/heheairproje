import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🌍 국가별 MBTI 비율",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# MBTI 16가지
mbti_columns = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# -----------------------------
# 제목
# -----------------------------
st.title("🌍 국가별 MBTI 비율 알아보기")
st.write("국가를 선택하면 해당 국가의 MBTI 분포를 한눈에 확인할 수 있어요! 🧠")

st.divider()

# -----------------------------
# 국가 선택
# -----------------------------
countries = sorted(df["Country"].dropna().unique())

selected_country = st.selectbox(
    "🌎 국가를 선택하세요",
    countries
)

# 선택한 국가 데이터
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI별 비율
mbti_values = pd.Series(
    {mbti: float(country_data[mbti]) for mbti in mbti_columns}
)

# 높은 순서대로 정렬
mbti_values = mbti_values.sort_values(ascending=False)

# -----------------------------
# 최고 MBTI 표시
# -----------------------------
top_mbti = mbti_values.index[0]
top_value = mbti_values.iloc[0] * 100

st.subheader(f"🏆 {selected_country}에서 가장 높은 MBTI")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "가장 높은 유형",
        top_mbti
    )

with col2:
    st.metric(
        "비율",
        f"{top_value:.2f}%"
    )

st.divider()

# -----------------------------
# 막대그래프
# -----------------------------
st.subheader(f"📊 {selected_country}의 MBTI 비율")

# 퍼센트로 변환
percent_values = mbti_values * 100

# 그래프 크기
fig, ax = plt.subplots(figsize=(12, 7))

# 1등 빨간색
# 나머지는 진한 파랑 → 연한 파랑 그라데이션
colors = []

for i in range(len(percent_values)):
    if i == 0:
        colors.append("#E53935")
    else:
        # 2등부터 점점 흐려지는 파란색
        progress = (i - 1) / max(len(percent_values) - 2, 1)

        # 진한 파랑에서 연한 파랑으로
        start = np.array([30, 100, 200])
        end = np.array([180, 220, 255])

        rgb = start * (1 - progress) + end * progress
        rgb = rgb.astype(int)

        colors.append(
            "#{:02X}{:02X}{:02X}".format(
                rgb[0], rgb[1], rgb[2]
            )
        )

# 막대그래프
bars = ax.bar(
    percent_values.index,
    percent_values.values,
    color=colors
)

# -----------------------------
# 그래프 꾸미기
# -----------------------------
ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=18,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("MBTI", fontsize=12)
ax.set_ylabel("비율 (%)", fontsize=12)

ax.set_ylim(
    0,
    max(percent_values.values) * 1.18
)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.25
)

ax.set_axisbelow(True)

# 막대 위에 퍼센트 표시
for bar, value in zip(bars, percent_values.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(percent_values.values) * 0.015,
        f"{value:.2f}%",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold"
    )

# 테두리 제거
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 순위표
# -----------------------------
st.subheader("🏅 MBTI 순위")

ranking_df = pd.DataFrame({
    "순위": range(1, 17),
    "MBTI": percent_values.index,
    "비율": [f"{value:.2f}%" for value in percent_values.values]
})

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True
)

st.caption("※ 위 데이터는 제공된 국가별 MBTI 비율 CSV 파일을 기반으로 합니다.")
