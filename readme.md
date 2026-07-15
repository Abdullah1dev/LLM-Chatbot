# 🤖 AI Chatbot with RAG, Human-in-the-Loop & Persistent Memory

An AI-powered chatbot built using **LangGraph**, **LangChain**, and **Streamlit** that supports Retrieval-Augmented Generation (RAG), persistent conversation memory, tool calling, streaming responses, and Human-in-the-Loop (HITL) workflows.

The chatbot allows users to upload PDF documents, ask questions about them, maintain multiple conversations, and safely execute sensitive actions through an approval workflow.

---

# ✨ Features

- 💬 Multi-thread conversations
- 🧠 Persistent memory using LangGraph Checkpointer (SQLite)
- 📄 Retrieval-Augmented Generation (RAG)
- 📚 PDF document upload and semantic search
- 🔍 Vector search using embeddings
- ⚡ Streaming AI responses
- 🛠 Tool Calling with LangGraph ToolNode
- 👨‍💻 Human-in-the-Loop approval system
- 🗑 Delete conversation with confirmation
- 🔄 Conversation resume using LangGraph Interrupts
- 🎯 Modular project architecture

---

# 🏗 Project Architecture

```
Chatbot/
│
├── app.py                     # Streamlit frontend
├── requirements.txt
│
├── src/
│   ├── graph.py               # LangGraph workflow
│   ├── nodes.py               # Graph nodes
│   ├── llm.py                 # LLM configuration
│   ├── tools.py               # LangGraph tools
│   ├── rag.py                 # RAG pipeline
│   ├── memory.py              # SQLite Checkpointer
│   ├── state.py               # Graph State
│   ├── helpers.py             # Utility functions
│   └── database/
│       └── chatbot.db
│
└── uploads/
```

---

# 🧩 Technologies Used

- Python
- Streamlit
- LangGraph
- LangChain
- OpenRouter
- SQLite
- FAISS
- HuggingFace Embeddings
- PyPDFLoader

---

# 🚀 Implemented Concepts

## LangGraph

- StateGraph
- Nodes
- Conditional Edges
- ToolNode
- tools_condition
- RunnableConfig
- Checkpointer
- SqliteSaver
- Thread IDs
- Persistent Memory

---

## Retrieval-Augmented Generation (RAG)

- PDF Upload
- PDF Parsing
- Document Chunking
- Embeddings
- FAISS Vector Store
- Semantic Retrieval

---

## Tool Calling

- Custom LangGraph Tools
- ToolNode
- Automatic Tool Selection

---

## Human-in-the-Loop (HITL)

Implemented a complete approval workflow using:

- interrupt()
- Command(resume=True)
- Command(resume=False)
- InjectedToolArg
- RunnableConfig

The chatbot pauses execution before performing sensitive operations (such as deleting a conversation), waits for user approval, and resumes execution from the exact checkpoint.

---

## Persistent Memory

Conversation history is stored using:

- SQLite
- LangGraph Checkpointer
- Thread-based conversation management

Users can:

- Start multiple conversations
- Resume previous chats
- Delete conversations safely

---

# 📂 Supported Features

✅ Chat with AI

✅ Upload PDF

✅ Ask questions from uploaded documents

✅ Persistent conversation history

✅ Streaming responses

✅ Multiple chat threads

✅ Conversation deletion

✅ Human approval before deletion

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/chatbot.git
```

Move into the project

```bash
cd chatbot
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
OPENAI_API_KEY=YOUR_OPENROUTER_KEY

OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

---

# 📌 Future Improvements

- Long-Term Memory
- MCP (Model Context Protocol)
- Multi-Agent Architecture
- Time Travel
- Conversation Summarization
- Authentication
- Cloud Deployment

---

# 📸 Demo

*(Add screenshots or GIFs here.)*

---

# 👨‍💻 Author

**Abdullah Tahir**

LinkedIn:
https://www.linkedin.com/in/abdullah-tahir-084307370

GitHub:
https://github.com/Abdullah1dev

---

## ⭐ If you found this project useful, consider giving it a star!
