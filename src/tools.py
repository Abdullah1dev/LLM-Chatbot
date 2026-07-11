from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from src.rag import retriever , set_retriever


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

