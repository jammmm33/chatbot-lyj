import streamlit as st
import uuid
from llm import get_ai_message

## 페이지 설정
st.set_page_config(page_title="청년수당 안내 챗봇", page_icon="😎")
st.title("청년수당 안내 챗봇😎")
st.markdown("---")

## 세션 초기화
query_params = st.query_params
if 'session_id' not in query_params:
    session_id = str(uuid.uuid4())
    st.query_params.update({'session_id': session_id})
else:
    session_id = query_params['session_id']

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = session_id

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

if 'clicked' not in st.session_state:
    st.session_state.clicked = None

## 자주 묻는 질문 버튼 목록
faq_list = [
    "청년수당이란?",
    "자기성장기록서란?",
    "카드 가능/불가능 사용처"
]

## 버튼 UI
st.markdown("### 📌 자주 묻는 질문")
cols = st.columns(len(faq_list))

for i, q in enumerate(faq_list):
    with cols[i]:
        if st.button(q):
            st.session_state.clicked = q

## 기존 메시지 출력
for message in st.session_state.message_list:
    with st.chat_message(message['role']):
        st.write(message['content'])

## 버튼 클릭 시 처리
if st.session_state.clicked:
    q = st.session_state.clicked
    with st.chat_message("user"):
        st.write(q)
    st.session_state.message_list.append({'role': 'user', 'content': q})

    with st.chat_message("ai"):
        with st.spinner("답변 생성 중..."):
            ai_response = get_ai_message(q)
            ai_message = st.write_stream(ai_response)

    st.session_state.message_list.append({'role': 'ai', 'content': ai_message})
    st.session_state.clicked = None 

## 채팅 입력창 입력 처리
if user_question := st.chat_input(placeholder="여기에 질문을 입력해주세요"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({'role': 'user', 'content': user_question})

    with st.chat_message("ai"):
        with st.spinner("답변 생성 중..."):
            ai_response = get_ai_message(user_question)
            ai_message = st.write_stream(ai_response)

    st.session_state.message_list.append({'role': 'ai', 'content': ai_message})

st.info("청년수당에 관한 궁금한 내용을 아래 채팅창에 입력해보세요!", icon="💬")

    