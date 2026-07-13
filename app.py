import streamlit as st
from src.graph import workflow , retrieve_all_threads ,  initialize_rag , set_retriever
from langchain_core.messages import HumanMessage
import uuid
from langgraph.types import Command


    



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
    state =  workflow.get_state(config =  {'configurable' : {'thread_id' : thread_id}} )      
    
    return state.values.get("messages" , [])



if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if  'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] =  retrieve_all_threads()
    
if 'retriever' not in st.session_state:
    st.session_state['retriever'] = None
    
if "uploaded_pdf_name" not in st.session_state:
    st.session_state["uploaded_pdf_name"] = None
    
    

if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False


if "approval_config" not in st.session_state:
    st.session_state.approval_config = None
    

if "interrupt_messages" not in st.session_state:
    st.session_state.interrupt_messages = None
    

add_thread(st.session_state['thread_id'])




config = {
    'configurable' : {'thread_id' : st.session_state['thread_id']},
    'meta_data' : {
        "thread_id" : st.session_state['thread_id']
    },
    
    "run_name" : "chatTurn"
    
    }



    
    
st.sidebar.title('LangGraph Chatbot')

uploaded_file  = st.sidebar.file_uploader(
    "Upload a PDF",
    type = ['pdf']
    
)

if uploaded_file:

    if st.session_state["uploaded_pdf_name"] != uploaded_file.name:

        retriever = initialize_rag(uploaded_file)

        st.session_state["retriever"] = retriever
        st.session_state["uploaded_pdf_name"] = uploaded_file.name

        set_retriever(retriever)

        st.success("PDF uploaded successfully!")




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
        

def is_action_required(user_input : str) -> bool:
    """
    Returns True if the request is an action that should not be streamed.
    """
    
    action_keywords = [
        "delete conversation",
        "delete this conversation",
        "remove conversation",
        "erase conversation",
    ]
    
    user_input = user_input.lower()
    
    
    return any(keyword in user_input for keyword in action_keywords)


if st.session_state.waiting_for_approval:
    st.warning(st.session_state.interrupt_messages)
    
    col1 , col2 = st.columns(2)
    
    with col1:
        if st.button("Yes"):
            result = workflow.invoke(
                Command(resume = True),
                config = st.session_state.approval_config 
                
            )
            
            st.session_state.waiting_for_approval = False
            st.session_state.approval_config = None
            st.session_state.interrupt_messages = None
            
            st.rerun()
    
    with col2:
        if st.button("No"):
            result = workflow.invoke(
                Command(resume = False),
                config = st.session_state.approval_config
                
            )
            st.session_state.waiting_for_approval = False
            st.session_state.approval_config = None
            st.session_state.interrupt_messages = None
            
            st.rerun()
            


if user_input:
    
    st.session_state['message_history'].append({'role' : 'user' , 'content' : user_input})
    with st.chat_message("user"):
         
        st.markdown(user_input)
    

    if is_action_required(user_input):
        result = workflow.invoke(
            {"messages" : [HumanMessage(content=user_input)]},
            config=config
            
            
        )
        if "__interrupt__" in result:
            st.session_state.waiting_for_approval = True
            st.session_state.approval_config = config
            st.session_state.interrupt_messages = result["__interrupt__"][0].value
            
            st.rerun()
        
    else:
        with st.chat_message('assistant'):
            ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in workflow.stream(
            {'messages' : [HumanMessage(content=user_input)]},
            config = config,
            stream_mode = 'messages'
        )
        )
        
        st.session_state['message_history'].append({'role' : 'assistant' , 'content' : ai_message})
        
        
    
    