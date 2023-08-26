# !pip install OpenAI langchain PyPDF2 tiktoken faiss-cpu grobid-client
# https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf

# (1) PDF 불러오기 및 텍스트 추출

from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

# .env 파일 로드
load_dotenv()

# 환경변수로부터 OpenAI API 키를 가져온다. 
openai_api_key = os.environ.get("OPENAI_API_KEY")

# PDF 파일을 PdfReader 클래스를 사용하여 열고 reader 변수에 저장한다.
reader = PdfReader("the_little_prince.pdf")

# 본문을 읽어 들인다.
raw_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text
print("[PDF 텍스트 추출 샘플]\n")
print(raw_text[:1000])


# (2) LangChain을 이용하여 줄거리 요약
from langchain import OpenAI
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain

llm = OpenAI(temperature=0)
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

summarize_document_chain.run(raw_text)


# (3) LangChain 질의 응답
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
model = ChatOpenAI(model="gpt-3.5-turbo-16k") # gpt-3.5-turbo-16k, gpt-4
qa_chain = load_qa_chain(model, chain_type="map_reduce")
qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)


# (4-1) 첫 번째 질문
# QA 실행
qa_document_chain.run(
    input_document=raw_text,
    question="줄거리를 요약해줘")


# (4-2) 두 번째 질문
# QA 실행
qa_document_chain.run(
    input_document=raw_text,
    question="주인공의 이름은?")

