### 0. 사업보고서 다운받기 ###

from dotenv import load_dotenv
import os
import OpenDartReader

# .env 파일 로드
load_dotenv()

# 객체 생성 (API KEY 지정)
api_key = os.getenv("DART_KEY")
dart = OpenDartReader(api_key)

# 종목코드, 조회기간 입력
dart_list = dart.list('022100', start='2018-01-01', end='2023-08-23', kind='A', final=False)

# 조회 기간 중 가장 최신 사업보고서의 idx
report_idx = dart_list['rcept_no'][0]

# 해당 idx에 해당하는 사업보고서 Raw Text 추출
xml_text = dart.document(report_idx)


import re # 전처리 함수

def extract_refine_text(html_string):
    # Remove CSS styles
    no_css = re.sub('<style.*?</style>', '', html_string, flags=re.DOTALL)

    # Remove Inline CSS
    no_inline_css = re.sub('\..*?{.*?}', '', no_css, flags=re.DOTALL)

    # Remove specific undesired strings
    no_undesired = re.sub('\d{4}[A-Za-z0-9_]*" ADELETETABLE="N">', '', no_inline_css)

    # Remove HTML tags
    no_tags = re.sub('<[^>]+>', ' ', no_undesired)

    # Remove special characters and whitespaces
    cleaned = re.sub('\s+', ' ', no_tags).strip()

    # Remove the □ character
    no_square = re.sub('□', '', cleaned)

    # Replace \' with '
    final_text = re.sub(r"\\'", "'", no_square)

    return final_text


refined_text = extract_refine_text(xml_text)
print(refined_text) # 텍스트 전처리 여부 확인


with open(f"재무제표_{report_idx}.txt", 'w', encoding='utf-8') as f:
          f.write(refined_text) # 텍스트 파일 저장