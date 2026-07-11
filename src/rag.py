from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS







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
    
    