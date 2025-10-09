 SAP Error Resolution Assistant (LLM + RAG Chatbot)

An on-premises LLM-based insights management system designed to understand and resolve SAP error codes using a Retrieval-Augmented Generation (RAG) pipeline and prompt-engineered chatbot interface.

 Project Overview

This project bridges enterprise SAP systems and modern AI architectures by integrating:

Local LLM (Llama 3.1 via Ollama) for intelligent text generation

RAG pipeline for accurate, context-aware responses

Python backend for data preparation and retrieval

Streamlit web interface for an intuitive, interactive chatbot experience

 Objectives

Build an on-premises chatbot that provides accurate, concise (max 250 words) SAP error explanations.

Use LLM-based insights management to extract actionable solutions from internal datasets.

Combine prompt engineering and semantic search to enhance response quality and precision.

 System Architecture

Data Source — Excel dataset containing SAP error codes and their solutions.

ETL Pipeline — Python + Pandas script processes and cleans the data.

Vector Store — ChromaDB stores text embeddings for similarity search.

Embedding Model — SentenceTransformers (MiniLM) encodes text into semantic vectors.

LLM Engine — Llama 3.1 (8B) running locally via Ollama.

RAG Flow — User query → Relevant context retrieval → Prompt + context → LLM-generated answer.

Frontend — Streamlit web app for user interaction.

⚙️ Technologies Used
Category	Tools
Language	Python
LLM Engine	Ollama (Llama 3.1 8B)
Frameworks	LangChain, Streamlit
Vector DB	ChromaDB
Embeddings	SentenceTransformers (MiniLM)
Data Processing	Pandas
Deployment	Local / On-Premises
 Key Features

✅ RAG-based Question Answering — Combines retrieval and generation for context-aware answers
✅ Prompt Engineering — Structured instructions ensure consistent, relevant responses
✅ Offline Deployment — Fully functional without cloud dependencies
✅ Interactive UI — Clean Streamlit interface for user-friendly interaction
✅ Scalable Architecture — Easily adaptable for HR, finance, or document-based assistants

 Business Value

Enables instant troubleshooting for SAP consultants and developers.

Reduces support time and knowledge dependency across teams.

Demonstrates how enterprise data can be transformed into intelligent insights using LLMs.

Serves as a foundation for building domain-specific AI copilots.

 Example Prompt

User: “How do I fix SAP error code VP199?”
Assistant: Retrieves context from the Excel dataset and returns a 250-word explanation including the root cause, solution steps, and reference link.

 How to Run Locally
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
