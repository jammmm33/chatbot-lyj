import uuid
import streamlit as st
from llm import get_ai_message

st.set_page_config(page_title='청년수당 안내문 챗', page_icon='😎')
st.title('청년수당 안내문 챗봇😎')
st.markdown("---")

query_params = st.query_params

if 'session_id' in query_params:
    session_id = query_params['session_id']
else:
    session_id = str(uuid.uuid4())
    st.query_params.update({'session_id': session_id})

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = session_id

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

## 이전 채팅 내용 화면 출력
for message in st.session_state.message_list:
    with st.chat_message(message['role']):
        st.write(message['content'])

## 채팅창
if user_question := st.chat_input(placeholder='여기에 질문을 입력해주세요'):
    with st.chat_message('user'):
        st.write(user_question)
    st.session_state.message_list.append({'role':'user', 'content': user_question})

    with st.spinner('답변을 생성하는 중입니다.'):
        ai_message = get_ai_message(user_question)

    with st.chat_message('ai'):
        ai_message = st.write_stream(ai_message)
    st.session_state.message_list.append({'role':'ai', 'content':ai_message})

st.info("청년수당에 관한 궁금한 내용을 아래 채팅창에 입력해보세요!", icon="💬")

    