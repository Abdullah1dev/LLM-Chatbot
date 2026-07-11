from langgraph.graph import StateGraph , START , END
import os
from langchain_core.messages import HumanMessage
from src.llm import model
from src.memory import checkpointer , retrieve_all_threads
from src.state import ChatState

from src.rag import embeddings , initialize_rag , set_retriever , retriever

from src.llm import model_with_tools
from src.tools import tools , ToolNode , tools_condition



    

def chatnode(state : ChatState):
    messages = state["messages"]
    
    response = model_with_tools.invoke(messages)
    
    return {'messages' : [response]}



tool_node = ToolNode(tools)

graph = StateGraph(ChatState)

graph.add_node('chatnode' , chatnode)
graph.add_node('tools' , tool_node)

graph.add_edge(START , 'chatnode')
graph.add_conditional_edges("chatnode" , tools_condition)
graph.add_edge("tools", "chatnode")

workflow = graph.compile(checkpointer = checkpointer)



