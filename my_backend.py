from langgraph.graph import StateGraph , START , END


import os

from langchain_core.messages import HumanMessage

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from src.llm import model
from src.memory import checkpointer , retrieve_all_threads
from src.state import ChatState



embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

retriever = None

def set_retriever(new_retriever):
    global retriever
    retriever = new_retriever
    

def initialize_rag(uploaded_file):
    os.makedirs("temp/" , exist_ok=True)
    
    try:
        
        pdf_path = os.path.join("temp/" , uploaded_file.name)
         
        with open(pdf_path , 'wb') as f:
            f.write(uploaded_file.getvalue())
            
        
        loader = PyPDFLoader(pdf_path)
        
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
        )
        
        chunks = text_splitter.split_documents(documents)
        
        vector_store = FAISS.from_documents(chunks , embeddings)
        
        retriever = vector_store.as_retriever(
        search_type = 'similarity',
        search_kwargs = {"k" : 4}
        
        )
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            
        
        
        return retriever 
    
    except Exception as e:
        raise e
    
    


@tool
def rag_tool(query : str) -> str:
    
    
    """
    Use the uploaded pdf and return relevant information to answer the user question
    Use this tool ONLY when the user is asking questions about the uploaded PDF or document.
    """
    
    print("RAG tool is executed")
    
    
    if retriever  is None:
        return "No document is currently available for retrievel"
    
    
    result = retriever.invoke(query)
    
    context = "\n\n".join(doc.page_content for doc in result)
    
    return context
    
    
    

tools = [rag_tool]
model_with_tools = model.bind_tools(tools)

tool_node = ToolNode(tools)






    
    

def chatnode(state : ChatState):
    messages = state["messages"]
    
    response = model_with_tools.invoke(messages)
    
    return {'messages' : [response]}





graph = StateGraph(ChatState)

graph.add_node('chatnode' , chatnode)
graph.add_node('tools' , tool_node)

graph.add_edge(START , 'chatnode')
graph.add_conditional_edges("chatnode" , tools_condition)
graph.add_edge("tools", "chatnode")

workflow = graph.compile(checkpointer = checkpointer)



