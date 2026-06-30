import streamlit as st
from backend import workflow , retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid



user_input = st.chat_input("Type Here")


def generate_threadid():
    thread_id = uuid.uuid4()
    return thread_id


def reset_history():
    st.session_state['thread_id'] = generate_threadid()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
    

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    return workflow.get_state(config =  {'configurable' : {'thread_id' : thread_id}} ).values['messages']       
    
    

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if  'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] =  retrieve_all_threads()
    
    
    

add_thread(st.session_state['thread_id'])




config = {'configurable' : {'thread_id' : st.session_state['thread_id']}}


    
    
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_history()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    
    
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        
        temp_messages = []
        
        for msg in messages:
            if isinstance(msg , HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            
            temp_messages.append({'role' : role , 'content' : msg.content})
        
        st.session_state['message_history'] = temp_messages
        
    
    

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