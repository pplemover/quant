## 주식 데이터 및 시각화 

본 프로젝트는 파이썬을 활용하여 주식 데이터를 분석하고 시각화하는 것을 목표로 합니다.

### 1. OpenDART로 최신 사업보고서 txt 파일 다운로드받기 : opendart.py

`OpenDartReader` 라이브러리를 활용하여 기업의 사업보고서를 다운로드하고, 해당 보고서의 텍스트 데이터를 전처리하여 파일로 저장합니다. 필요한 라이브러리는 다음과 같습니다. 
```
pip install OpenDartReader
```

API 키를 지정한 뒤, `list` 함수를 사용하여 특정 종목의 사업 보고서 리스트를 가져올 수 있습니다. 
```Python
import OpenDartReader

# API KEY 설정
api_key = 'YOUR_API_KEY'
dart = OpenDartReader(api_key)

# 종목코드, 조회기간 입력
dart_list = dart.list('022100', start='2018-01-01', end='2023-08-23', kind='A', final=False)

# 최신 사업보고서의 idx 추출
report_idx = dart_list['rcept_no'][0]

# 해당 idx에 해당하는 사업보고서 Raw Text 추출
xml_text = dart.document(report_idx)
```

이후 `re` 라이브러리를 이용하여 수집한 사업보고서의 XML 텍스트를 전처리합니다.
```Python
import re

def extract_refine_text(html_string):
    # 전처리 과정 생략 (CSS 제거, HTML 태그 제거, 불필요한 문자 제거 등)

    return final_text

refined_text = extract_refine_text(xml_text)
```

마지막으로 전처리한 텍스트 데이터를 텍스트 파일로 저장합니다.
```Python
with open(f"재무제표_{report_idx}.txt", 'w', encoding='utf-8') as f:
    f.write(refined_text)
```

### 2. 캔들차트 만들기 : candlechart.py

`FinanceDataReader` 라이브러리를 활용하여 KRX 주식 데이터를 가져와 분석하고 시각화하였습니다. 필요한 라이브러리는 다음과 같습니다.
```
pip install FinanceDataReader pandas matplotlib
```

`StockListing` 함수를 통해 KRX의 주식 리스트를 가져와 stockList.csv 파일로 저장할 수 있습니다.
```Python
import FinanceDataReader as fdr

df_krx = fdr.StockListing('KRX')
df_krx.to_csv('stockList.csv', mode='w', encoding='utf-8-sig')
```

아래의 코드를 실행하면 주식 데이터의 캔들 차트와 이동평균선, 거래량 변동을 한눈에 확인할 수 있는 그래프가 생성됩니다. 
```Python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(16, 14))
top_axes = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
bottom_axes = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)

top_axes.plot(df.index, df['5일'], label='5일', color='purple', linewidth=1.5)
# 이하 생략 (20일, 60일, 120일, 240일에 대한 이동평균선 추가)

top_axes.plot(df.index, df['Close'], linewidth=1)
top_axes.bar(df.index, height=df['Close'] - df['Open'], bottom=df['Open'], width=1, color=list(map(lambda c: 'red' if c > 0 else 'blue', df['Change'])))
top_axes.vlines(df.index, df['Low'], df['High'], color=list(map(lambda c: 'red' if c > 0 else 'blue', df['Change'])))

bottom_axes.bar(df.index, df['Volume'])

plt.show()
```

### 3. 파이썬 Streamlit 라이브러리를 통해서 Web applicatin으로 구현하기 : streamlit.py


### 4. 데이터 웹 앱 솔루션 (Gradio, Streamlit)





