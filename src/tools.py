from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from src.rag import retriever , set_retriever
from langgraph.types import interrupt



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
    
    

@tool
def  delete_conversation() -> str:
    
    
    """
    Delete a conversation using its thread ID.
    This tool should only be used when the user explicitly requests to delete a conversation.
    """
    
    approval = interrupt(
        "Do you reallly want to Delete this conversation??"
        
    )
    
    print("Approval recieved" , approval)
    
    
    
    
    return "Delete tool executed"



    
    

tools = [rag_tool , delete_conversation]


