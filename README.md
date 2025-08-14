# 청년수당 안내문 AI 챗봇 💬

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/) [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![LangChain](https://img.shields.io/badge/LangChain-0086D1?style=for-the-badge)](https://www.langchain.com/) [![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/) [![Pinecone](https://img.shields.io/badge/Pinecone-0C59E8?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io/)

> 서울시 청년수당 안내문(`chungnun.docx`) 문서를 기반으로 사용자의 질문에 답변하는 RAG(검색 증강 생성) 기반의 AI 챗봇입니다. LangChain과 OpenAI, Pinecone을 활용하여 문서에 대한 자연어 질의응답 기능을 구현하고 Streamlit을 통해 웹 애플리케이션으로 배포했습니다.
> 
> **배포 주소:** https://chatbot-lyj-250618.streamlit.app

<br>

## **📜 프로젝트 정보**

-   **프로젝트 기간:** 2025.06.13 ~ 2025.06.22
-   **주요 목표:** 특정 문서(서울시 청년수당 안내문)에 대한 정보를 효과적으로 전달하는 문서 기반 Q&A 챗봇 개발

## **✨ 주요 기능**

-   **💬 자연어 질의응답:** 청년수당과 관련된 질문을 자유롭게 입력하면, AI가 안내문 내용을 바탕으로 답변을 생성합니다.
-   **🧠 RAG(검색 증강 생성) 적용:** 사용자의 질문과 가장 관련성 높은 문서 내용을 Pinecone 벡터 DB에서 검색한 후, 이 정보를 참고하여 OpenAI LLM이 정확하고 일관된 답변을 생성합니다.
-   **💡 Few-Shot 프롬프팅:** `config.py`에 정의된 질의응답 예시를 프롬프트에 포함하여, AI가 더 정확한 형식과 톤으로 답변하도록 유도합니다.
-   **📚 용어사전 기능:** `keyword_dictionary.json`에 정의된 주요 용어(청년수당, 자기성장기록서 등)를 답변 생성 시 참고하여, 더 풍부하고 정확한 정보를 제공합니다.
-   **📌 FAQ 기능:** 자주 묻는 질문들을 버튼으로 제공하여 사용자가 쉽게 원하는 정보를 얻을 수 있도록 돕습니다.
-   **🔒 비속어 필터링:** 간단한 비속어 필터링 기능을 구현하여 부적절한 언어 사용을 방지합니다.
-   **🌐 웹 배포:** `Streamlit`을 사용하여 개발된 챗봇을 간편하게 웹 애플리케이션으로 배포하고 상호작용할 수 있도록 구현했습니다.

## **🛠️ 기술 스택**

-   **언어:** `Python`
-   **AI 프레임워크:** `LangChain`
-   **LLM:** `OpenAI GPT-4o`
-   **임베딩 모델:** `OpenAI text-embedding-3-large`
-   **벡터 데이터베이스:** `Pinecone`
-   **웹 프레임워크:** `Streamlit`
-   **핵심 라이브러리:** `langchain-openai`, `langchain-pinecone`, `streamlit`, `python-dotenv`

## **🏛️ 시스템 작동 원리**

1.  **문서 임베딩 (준비 단계):** `chungnun.docx` 문서를 텍스트로 변환하고, 의미 단위로 분할(Chunking)한 뒤, OpenAI 임베딩 모델을 통해 벡터로 변환하여 Pinecone 벡터 DB에 저장합니다.
2.  **사용자 질문 입력:** 사용자가 Streamlit 웹 앱에서 질문을 입력합니다.
3.  **유사도 검색 (Retrieval):** LangChain이 사용자의 질문을 벡터로 변환한 후, Pinecone DB에서 의미적으로 가장 유사한 문서 조각들을 검색합니다.
4.  **프롬프트 생성:** 검색된 문서 조각(Context), `config.py`의 질의응답 예시, `keyword_dictionary.json`의 용어 정의를 모두 포함하는 정교한 프롬프트를 동적으로 생성합니다.
5.  **답변 생성 (Generation):** 생성된 프롬프트를 OpenAI GPT-4o 모델에 전달하여, 주어진 정보를 바탕으로 최종 답변을 생성합니다.
6.  **답변 출력:** 생성된 답변을 Streamlit의 `write_stream` 기능을 통해 타이핑 효과와 함께 사용자에게 보여줍니다.

<br>
