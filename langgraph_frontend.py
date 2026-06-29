import streamlit as st
from langgraph_backend import workflow
from langchain_core.messages import HumanMessage
import uuid


user_input = st.chat_input("Type Here")


#utitlity funtion

def generate_threadid():
    thread_id = uuid.uuid4()
    return thread_id


def reset_history():
    st.session_state['thread_id'] = generate_threadid()
    st.session_state['message_history'] = []
    
    
    

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()




config = {'configurable' : {'thread_id' : st.session_state['thread_id']}}


    
    
    
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_history()

st.sidebar.header('My Conversations')

st.sidebar.text(st.session_state['thread_id'])





for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
        


if user_input:
    
    st.session_state['message_history'].append({'role' : 'user' , 'content' : user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    
    
    

    
    
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in workflow.stream(
            {'messages' : [HumanMessage(content=user_input)]},
            config = config,
            stream_mode = 'messages'
        )
        )
        
    st.session_state['message_history'].append({'role' : 'assistant' , 'content' : ai_message})
     