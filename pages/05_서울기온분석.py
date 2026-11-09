import pandas as pd

# 한글 인코딩 처리
df = pd.read_csv('temperature.csv', encoding='cp949')

# 모든 기온 데이터가 비어 있는 행 제거
temperature_cols = df.columns[1:]
df = df.dropna(subset=temperature_cols, how='all')

# 기온 데이터 결측치 확인
print(df.isnull().sum())

# 통계 분석
print(df.describe())

# UTF-8 인코딩으로 저장
df.to_csv(
    'temperature_utf8.csv',
    index=False,
    encoding='utf-8-sig'
)
