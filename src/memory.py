from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3



conn = sqlite3.connect('database/chatbot.db' , check_same_thread=False)

checkpointer = SqliteSaver(conn = conn)


def retrieve_all_threads():
    print("Function Defined")
    
    all_threads = set()
    
    
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    return list(all_threads)


def delete_thread(thread_id : str):
    checkpointer.delete_thread(thread_id)
    
    
        
        
