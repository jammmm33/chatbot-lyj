import streamlit as st

st.set_page_config(page_title='아직 생각중인 챗봇', page_icon='😎')
st.title('아직 생각중인 챗봇😎')

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

with st.chat_message('ai'):
    st.write('여기는 AI 메시지')
st.session_state.message_list.append({'role':'ai', 'content':'여기는 AI 메시지'})
    