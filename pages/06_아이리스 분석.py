
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# -----------------------------------
# 1. 페이지 설정
# -----------------------------------

st.set_page_config(
    page_title="아이리스 품종 예측 AI",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 AI 아이리스 품종 예측")
st.write(
    "꽃잎의 길이와 너비를 입력하면 "
    "인공지능이 붓꽃의 품종을 예측해 줘!"
)

st.divider()


# -----------------------------------
# 2. CSV 파일 불러오기
# -----------------------------------

@st.cache_data
def load_data():

    # pages 폴더의 상위 폴더에서 CSV 찾기
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "아이리스.csv"
    )

    # 한글 인코딩 처리
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "아이리스.csv 파일을 찾을 수 없습니다. "
        "pages 폴더의 상위 폴더에 CSV 파일을 넣어 주세요."
    )
    st.stop()


# -----------------------------------
# 3. 데이터 전처리
# -----------------------------------

required_columns = [
    "꽃잎길이",
    "꽃잎너비",
    "품종"
]

for col in required_columns:
    if col not in df.columns:
        st.error(f"CSV 파일에 '{col}' 컬럼이 없습니다.")
        st.stop()

df = df[required_columns].copy()

df["꽃잎길이"] = pd.to_numeric(
    df["꽃잎길이"], errors="coerce"
)

df["꽃잎너비"] = pd.to_numeric(
    df["꽃잎너비"], errors="coerce"
)

df["품종"] = df["품종"].astype(str)

df = df.dropna()

df = df[df["품종"].isin([
    "Iris-setosa",
    "Iris-versicolor",
    "Iris-virginica"
])]

if df.empty:
    st.error("분석할 수 있는 데이터가 없습니다.")
    st.stop()


# -----------------------------------
# 4. 머신러닝 데이터 준비
# -----------------------------------

X = df[["꽃잎길이", "꽃잎너비"]]
y = df["품종"]

# 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 5. 랜덤 포레스트 모델 생성
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=5
)

model.fit(X_train, y_train)

# 모델 정확도
y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)


# -----------------------------------
# 6. 품종 이름과 그래프 색상
# -----------------------------------

species_names = {
    "Iris-setosa": "세토사",
    "Iris-versicolor": "버시컬러",
    "Iris-virginica": "버지니카"
}

species_colors = {
    "Iris-setosa": "#FF6B6B",
    "Iris-versicolor": "#4ECDC4",
    "Iris-virginica": "#6C63FF"
}


# -----------------------------------
# 7. 사용자 입력 화면
# -----------------------------------

st.subheader("✏️ 꽃잎 크기 입력하기")

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "🌷 꽃잎 길이 (cm)",
        min_value=0.1,
        max_value=7.9,
        value=4.5,
        step=0.1
    )

with col2:
    petal_width = st.number_input(
        "🌼 꽃잎 너비 (cm)",
        min_value=0.1,
        max_value=2.8,
        value=1.5,
        step=0.1
    )

predict_button = st.button(
    "🔍 품종 예측하기",
    type="primary",
    use_container_width=True
)


# -----------------------------------
# 8. 예측 결과
# -----------------------------------

if predict_button:

    user_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎길이", "꽃잎너비"]
    )

    # 품종 예측
    prediction = model.predict(user_data)[0]

    # 품종별 예측 확률
    probabilities = model.predict_proba(user_data)[0]

    probability_df = pd.DataFrame({
        "품종": model.classes_,
        "확률": probabilities
    })

    probability_df["한글 품종"] = (
        probability_df["품종"].map(species_names)
    )

    probability_df = probability_df.sort_values(
        "확률",
        ascending=False
    )

    st.divider()

    st.subheader("🎉 AI 예측 결과")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric(
            "예측된 붓꽃 품종",
            species_names[prediction]
        )

    with result_col2:
        st.metric(
            "예측 확률",
            f"{probabilities[list(model.classes_).index(prediction)] * 100:.1f}%"
        )

    st.success(
        f"🌸 입력한 꽃은 "
        f"**{species_names[prediction]}** 품종으로 예측되었어!"
    )

    # -----------------------------------
    # 9. 결정 영역 시각화
    # -----------------------------------

    st.subheader("📊 품종 분류 영역 시각화")

    st.write(
        "배경 색상은 AI가 각 위치를 어떤 품종으로 "
        "분류하는지 보여줘. 별은 네가 입력한 꽃의 위치야."
    )

    x_min = min(
        df["꽃잎길이"].min(),
        petal_length
    ) - 0.3

    x_max = max(
        df["꽃잎길이"].max(),
        petal_length
    ) + 0.3

    y_min = min(
        df["꽃잎너비"].min(),
        petal_width
    ) - 0.2

    y_max = max(
        df["꽃잎너비"].max(),
        petal_width
    ) + 0.2

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 180),
        np.linspace(y_min, y_max, 180)
    )

    grid_data = pd.DataFrame({
        "꽃잎길이": xx.ravel(),
        "꽃잎너비": yy.ravel()
    })

    grid_prediction = model.predict(
        grid_data
    )

    class_numbers = {
        name: i for i, name in enumerate(model.classes_)
    }

    zz = np.array([
        class_numbers[name]
        for name in grid_prediction
    ]).reshape(xx.shape)

    # 결정 영역 그래프
    fig = go.Figure()

    fig.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, 180),
            y=np.linspace(y_min, y_max, 180),
            z=zz,
            colorscale=[
                [0.0, "#FFB3B3"],
                [0.333, "#FFB3B3"],
                [0.334, "#A8E6CF"],
                [0.666, "#A8E6CF"],
                [0.667, "#C9B6FF"],
                [1.0, "#C9B6FF"]
            ],
            showscale=False,
            contours=dict(
                coloring="fill",
                showlines=False
            ),
            hoverinfo="skip",
            opacity=0.55
        )
    )

    # 기존 데이터 산점도
    for species in model.classes_:

        species_df = df[
            df["품종"] == species
        ]

        fig.add_trace(
            go.Scatter(
                x=species_df["꽃잎길이"],
                y=species_df["꽃잎너비"],
                mode="markers",
                name=species_names[species],
                marker=dict(
                    size=8,
                    color=species_colors[species],
                    opacity=0.75
                ),
                hovertemplate=(
                    "꽃잎 길이: %{x} cm<br>"
                    "꽃잎 너비: %{y} cm"
                    "<extra>" + species_names[species] + "</extra>"
                )
            )
        )

    # -----------------------------------
    # 10. 무지개색 별 표시
    # -----------------------------------

    rainbow_colors = [
        "#FF0000",
        "#FF7F00",
        "#FFFF00",
        "#00CC44",
        "#0088FF",
        "#4B0082",
        "#9400D3"
    ]

    rainbow_sizes = [
        46, 40, 34, 28, 22, 16, 10
    ]

    for color, size in zip(
        rainbow_colors,
        rainbow_sizes
    ):

        fig.add_trace(
            go.Scatter(
                x=[petal_length],
                y=[petal_width],
                mode="markers",
                marker=dict(
                    symbol="star",
                    size=size,
                    color=color,
                    line=dict(
                        color="white",
                        width=0.5
                    )
                ),
                name="내가 입력한 꽃",
                showlegend=False,
                hovertemplate=(
                    "내가 입력한 꽃<br>"
                    "꽃잎 길이: %{x} cm<br>"
                    "꽃잎 너비: %{y} cm"
                    "<extra>예측 위치</extra>"
                )
            )
        )

    # 그래프 꾸미기
    fig.update_layout(
        title="🌈 꽃잎 크기에 따른 아이리스 품종 분류",
        xaxis_title="꽃잎 길이 (cm)",
        yaxis_title="꽃잎 너비 (cm)",
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[y_min, y_max]),
        template="plotly_white",
        height=650,
        legend_title="붓꽃 품종",
        hovermode="closest"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------
    # 11. 품종별 예측 확률
    # -----------------------------------

    st.subheader("🎯 품종별 예측 확률")

    prob_fig = px.bar(
        probability_df,
        x="한글 품종",
        y="확률",
        color="한글 품종",
        color_discrete_map={
            "세토사": "#FF6B6B",
            "버시컬러": "#4ECDC4",
            "버지니카": "#6C63FF"
        },
        text=probability_df["확률"].map(
            lambda x: f"{x * 100:.1f}%"
        )
    )

    prob_fig.update_layout(
        xaxis_title="붓꽃 품종",
        yaxis_title="예측 확률",
        yaxis=dict(
            tickformat=".0%",
            range=[0, 1]
        ),
        showlegend=False,
        template="plotly_white"
    )

    st.plotly_chart(
        prob_fig,
        use_container_width=True
    )

    # -----------------------------------
    # 12. 왜 이 품종으로 예측했을까?
    # -----------------------------------

    st.subheader("💡 왜 이 품종으로 분류되었을까?")

    st.write(
        f"""
        네가 입력한 꽃잎 크기는 다음과 같아.

        - 꽃잎 길이: **{petal_length} cm**
        - 꽃잎 너비: **{petal_width} cm**

        랜덤 포레스트는 학습한 여러 결정 트리의
        예측 결과를 종합해서 품종을 결정해.

        입력한 위치가 그래프에서
        **{species_names[prediction]} 영역**에 있기 때문에
        이 품종으로 예측된 거야.
        """
    )

    # 품종별 확률 설명
    for _, row in probability_df.iterrows():

        st.write(
            f"🌼 {row['한글 품종']}: "
            f"{row['확률'] * 100:.1f}%"
        )

        st.progress(
            float(row["확률"])
        )

    # -----------------------------------
    # 13. 특성 중요도
    # -----------------------------------

    st.subheader("🔎 어떤 특성이 중요할까?")

    importance_df = pd.DataFrame({
        "특성": ["꽃잎 길이", "꽃잎 너비"],
        "중요도": model.feature_importances_
    })

    importance_fig = px.bar(
        importance_df,
        x="중요도",
        y="특성",
        orientation="h",
        color="특성",
        color_discrete_sequence=[
            "#FF9A76",
            "#7B9FF2"
        ],
        text=importance_df["중요도"].map(
            lambda x: f"{x * 100:.1f}%"
        )
    )

    importance_fig.update_layout(
        title="랜덤 포레스트 특성 중요도",
        xaxis_title="중요도",
        yaxis_title="",
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(
        importance_fig,
        use_container_width=True
    )

    st.info(
        "특성 중요도는 모델이 전체 학습 데이터에서 "
        "각 특성을 분류에 얼마나 활용했는지 나타내는 값이야. "
        "개별 예측의 직접적인 원인을 뜻하지는 않아."
    )

    # -----------------------------------
    # 14. 모델 정확도
    # -----------------------------------

    st.divider()

    st.subheader("🤖 AI 모델 성능")

    st.metric(
        "테스트 데이터 예측 정확도",
        f"{accuracy * 100:.1f}%"
    )

    st.caption(
        "전체 데이터를 학습용과 테스트용으로 8:2 분리하여 "
        "측정한 정확도야."
    )

else:

    st.info(
        "👆 꽃잎 길이와 너비를 입력한 후 "
        "'품종 예측하기' 버튼을 눌러 줘!"
    )

# -----------------------------------
# 15. 하단 안내
# -----------------------------------

st.divider()

st.caption(
    "🌸 Iris AI Classification | "
    "Pandas + Scikit-learn + Plotly + Streamlit"
)
