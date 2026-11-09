import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="월별기온분석", page_icon="🌡️", layout="wide")

st.title("🌡️ 월별기온분석")
st.write("원하는 월을 선택하면 해당 월의 연도별 최고기온과 최저기온을 비교할 수 있어요.")

# CSV 파일은 app.py와 같은 폴더에 저장하세요.
DATA_FILE = Path(__file__).parent / "temperature.csv"

@st.cache_data
def load_data(file_path):
    # 원본 CSV의 한글 인코딩(CP949)을 먼저 시도하고,
    # UTF-8 BOM 파일도 읽을 수 있도록 예외 처리합니다.
    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    required_columns = ["일시", "최고기온(℃)", "최저기온(℃)"]
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(
            "CSV 파일에 필요한 열이 없습니다: " + ", ".join(missing)
        )

    # 일시 형식은 예: Oct-07, Nov-07
    # 영어 월 이름을 직접 변환해 서버의 로캘 설정에 영향을 받지 않게 합니다.
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    date_parts = data["일시"].astype(str).str.strip().str.split("-", expand=True)
    if date_parts.shape[1] < 2:
        raise ValueError("일시 열의 날짜 형식을 확인해 주세요. 예: Oct-07")

    month_text = date_parts[0].str[:3].str.title()
    year_text = date_parts[1].str.strip()

    data["월"] = month_text.map(month_map)
    data["연도"] = pd.to_numeric(year_text, errors="coerce")
    # 이 데이터의 연도 표기(07~26)는 2000년대 기준으로 변환합니다.
    data["연도"] = data["연도"].apply(
        lambda year: int(year) + 2000 if pd.notna(year) and year < 100 else year
    )

    data["최고기온(℃)"] = pd.to_numeric(data["최고기온(℃)"], errors="coerce")
    data["최저기온(℃)"] = pd.to_numeric(data["최저기온(℃)"], errors="coerce")

    data = data.dropna(subset=["월", "연도"])
    data["월"] = data["월"].astype(int)
    data["연도"] = data["연도"].astype(int)
    return data


if not DATA_FILE.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다. app.py와 같은 폴더에 업로드해 주세요.")
    st.stop()

try:
    df = load_data(DATA_FILE)
except Exception as error:
    st.error(f"데이터를 불러오는 중 문제가 발생했습니다: {error}")
    st.stop()

month_names = {
    1: "1월", 2: "2월", 3: "3월", 4: "4월",
    5: "5월", 6: "6월", 7: "7월", 8: "8월",
    9: "9월", 10: "10월", 11: "11월", 12: "12월"
}

selected_month_label = st.selectbox(
    "📅 분석할 월을 선택하세요",
    options=[month_names[m] for m in range(1, 13)],
    index=0
)
selected_month = [month for month, label in month_names.items()
                  if label == selected_month_label][0]

monthly = df[df["월"] == selected_month].copy()

# 같은 연도·월 자료가 여러 개라면 최고기온은 최댓값,
# 최저기온은 최솟값으로 연도별 집계합니다.
yearly = (
    monthly.groupby("연도", as_index=False)
    .agg({
        "최고기온(℃)": "max",
        "최저기온(℃)": "min"
    })
    .sort_values("연도")
)
