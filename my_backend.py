from langgraph.graph import StateGraph , START , END


import os

from langchain_core.messages import HumanMessage




from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from src.llm import model
from src.memory import checkpointer , retrieve_all_threads
from src.state import ChatState

from src.rag import embeddings , initialize_rag , set_retriever , retriever

    




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



