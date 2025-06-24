import os
import uuid
import streamlit as st
from llm import get_ai_message

# 페이지 설정
st.set_page_config(page_title="청년수당 안내문 챗봇", page_icon="😎")
st.title("청년수당 안내문 챗봇 😎")
st.markdown("---")

# 세션 ID 설정
query_params = st.query_params

if 'session_id' in query_params:
    session_id = query_params['session_id']
else:
    session_id = str(uuid.uuid4())
    st.query_params.update({'session_id': session_id})

## streamlit 내부 세션: session id 저장
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = session_id

## streamlit 내부 세션: 메시지 리스트 초기화
if 'message_list' not in st.session_state:
    st.session_state.message_list = []


# 🔶 FAQ 리스트
faq_list = [
    "청년수당이란?",
    "자기성장기록서란?",
    "카드 가능/불가능 사용처"
]

# 🔶 질문 입력 변수 초기화
user_question = None

# 🔶 FAQ 버튼 UI
st.subheader("📌 자주 묻는 질문")
cols = st.columns(len(faq_list))
for i, q in enumerate(faq_list):
    with cols[i]:
        if st.button(q):
            user_question = q

# 🔶 채팅 입력창
chat_input = st.chat_input(placeholder="여기에 질문을 입력해주세요")
if chat_input:
    user_question = chat_input


# 🔶 이전 대화 내용 출력 (→ FAQ 아래에서 출력)
for message in st.session_state.message_list:
    with st.chat_message(message['role']):
        st.write(message['content'])

# 🔶 질문이 들어온 경우 처리
if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({'role': 'user', 'content': user_question})

    with st.spinner('답변을 생성하는 중입니다.'):
        session_id = st.session_state.session_id
        ai_message = get_ai_message(user_question, session_id=session_id)

    with st.chat_message("ai"):
        ai_message = st.write_stream(ai_message)
    st.session_state.message_list.append({'role': 'ai', 'content': ai_message})
        

st.info("청년수당에 관한 궁금한 내용을 아래 채팅창에 입력해보세요!", icon="💬")

    