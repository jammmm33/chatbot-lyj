import os

from dotenv import load_dotenv
from langchain.chains import (create_history_aware_retriever,
                              create_retrieval_chain)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotPromptTemplate, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from config import answer_examples 


# 환경 변수 로딩
load_dotenv()


def get_llm(model='gpt-4o'):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model=model)
    return llm


def get_database():

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    index_name = "chungnun"

    # 벡터스토어에 인엑스 가져오기
    database = PineconeVectorStore.from_existing_index(
        embedding=embedding,
        index_name=index_name
    )
    return database


store = {}

def get_seesion_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_history_retriever(llm, retriever):
    contextualize_q_system_prompt = (
    '''채팅 히스토리와 가장 최근 사용자의 질문이 주어졌을 때,  
    그 질문이 이전 대화의 문맥을 참고할 수 있다는 점을 고려하여,  
    이전 히스토리 없이도 이해 가능한 독립적인 질문으로 바꿔주세요.  
    질문에 답변하지는 마세요.  
    필요하다면 문장을 재작성하고, 그렇지 않으면 그대로 반환하세요.'''
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )

    history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
    )

    return history_aware_retriever


def few_shot_examples() -> str:
    example_prompt = PromptTemplate.from_template("Question: {input}\n\nAnswer: {answer}")

    few_shot_prompt = FewShotPromptTemplate(
        examples=answer_examples,         
        example_prompt=example_prompt,    
        prefix='다음 질문에 답변하세요.', 
        suffix="Question: {input}",       
        input_variables=["input"],  
    )
    return few_shot_prompt.format(input = '{input}')


def get_qa_prompt():
    system_prompt = (
         '''
    -당신은 청년수당에 대한 안내문 입니다. 
    -[context]를 참고하여 사용자의 질문에 답변하세요.
    -청년수당 안내문에 대한 정보 이외에는 '답변을 할 수 없습니다.' 로 답하세요.
    -필요하다면 문서에서 직접 인용하거나 요약된 내용을 덧붙이세요.
    -사용자가 '알려주세요', '설명해주세요'  질문에도 답변하세요.
    -항목별로 표시해서 답변해주세요.
    
    [context]
    {context} 
    '''
    )

    formmated_few_shot_prompt = few_shot_examples()

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ('assistant', formmated_few_shot_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    return qa_prompt


def build_chain():
    llm = get_llm()

    database = get_database()
    retriever = database.as_retriever()

    history_aware_retriever = get_history_retriever(llm, retriever)
    qa_prompt = get_qa_prompt()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_seesion_history,
        input_messages_key='input',
         history_messages_key="chat_history",
        output_messages_key="answer",
        ).pick('answer')
    
    return conversational_rag_chain


def get_ai_message(user_message, session_id = 'default'):
    qa_chain = build_chain()

    ai_message = qa_chain.stream(
        {'input': user_message},
        config={"configurable": {"session_id": session_id}}
    )

    return ai_message
