# 🕉️ Mahabharata RAG

A Retrieval-Augmented Generation (RAG) system that allows users to ask questions about the **Mahabharata** and receive answers grounded in the original text.

The project combines **semantic search, vector embeddings, ChromaDB, and a local Large Language Model (LLM)** to retrieve relevant passages before generating an answer.

---

## 🚀 Project Overview

Traditional LLMs can sometimes generate incorrect or hallucinated information.

This project uses **Retrieval-Augmented Generation (RAG)** to solve that problem.

Instead of asking the LLM to answer directly:

User Question
↓
Semantic Search
↓
Relevant Mahabharata Passages
↓
Context + Question
↓
LLM
↓
Grounded Answer

The system retrieves relevant passages from the Mahabharata before generating the final response.

---

## 🧠 Architecture

```text
                    ┌─────────────────────┐
                    │   Mahabharata PDF   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Data Cleaning    │
                    │     clean.py        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Section Chunking  │
                    │     chunk.py        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Sentence           │
                    │  Transformers       │
                    │  Embeddings         │
                    │     embed.py        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Query Embedding    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │    retrieve.py      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Retrieved Context   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        LLM          │
                    │    generate.py      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Final Answer      │
                    └─────────────────────┘


✨ Features
📖 Mahabharata text processing
🧹 Automated text cleaning
✂️ Section-based document chunking
🔄 Overlapping chunks for better contextual retrieval
🧠 Semantic embeddings using Sentence Transformers
🔍 Vector similarity search
🗄️ ChromaDB vector database
🤖 Local LLM-based answer generation
📚 Answers grounded in retrieved Mahabharata passages
💻 Fully local RAG pipeline
🔐 No paid LLM API required


🛠️ Tech Stack

        Programming Language
        Python
        Machine Learning / AI
        Sentence Transformers
        Hugging Face Transformers
        PyTorch
        Local LLM
        Vector Database
        ChromaDB
        Data Processing
        Python
        Regular Expressions
        JSON
        Development
        Git
        GitHub
        VS Code
        Python Virtual Environment

📂 Project Structure

Mahabharata-rag/
│
├── data/
│   ├── raw/
│   │   └── Mahabharata.pdf
│   │
│   ├── processed/
│   │   ├── mahabharata.txt
│   │   ├── mahabharata_clean.txt
│   │   ├── chunks.json
│   │   └── embeddings.json
│   │
│   └── chroma_db/
│
├── src/
│   ├── scrape.py
│   ├── clean.py
│   ├── chunk.py
│   ├── embed.py
│   ├── vector_store.py
│   ├── retrieve.py
│   └── generate.py
|
|
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
|
|
│
├── requirements.txt
├── .gitignore
└── README.md

Generated datasets, embeddings, and the local ChromaDB database are excluded from Git using .gitignore.


⚙️ Installation

    1. Clone the repository
        git clone https://github.com/Barath-co/Mahabharata-rag.git
        cd Mahabharata-rag
    2. Create a virtual environment
        python -m venv venv
    3. Activate the virtual environment
        Windows PowerShell
        .\venv\Scripts\Activate.ps1
    4. Install dependencies
        pip install -r requirements.txt


🔄 RAG Pipeline

    Step 1 — Obtain the Mahabharata text

        The source text is converted into a text format that can be processed by the pipeline.

        python src/scrape.py
    Step 2 — Clean the text
        python src/clean.py

        The cleaning process normalizes whitespace and removes unwanted formatting.

    Step 3 — Create chunks
        python src/chunk.py

        The Mahabharata is divided into sections.

        Each section becomes a retrieval chunk with a small overlap between neighboring chunks to preserve contextual continuity.

    Step 4 — Generate embeddings
        python src/embed.py

        The project uses a Sentence Transformer model to convert text into numerical vectors.

        Current embedding size:

        384 dimensions

        The embeddings allow semantic similarity search rather than simple keyword matching.

    Step 5 — Store embeddings in ChromaDB
        python src/vector_store.py

        The embeddings and corresponding text chunks are stored inside ChromaDB.

        Current database:

        Collection: mahabharata
        Vectors: 5,161
        Embedding dimensions: 384
        Step 6 — Retrieve relevant passages
        python src/retrieve.py

        Example:

        Question: who was arjuna

        The system converts the question into an embedding and searches ChromaDB for the most semantically relevant passages.

        Example retrieval:

        RESULT 1
        Section: SECTION XXXVIII
        Distance: 0.638803

        RESULT 2
        Section: SECTION XXVIII
        Distance: 0.732080
        Step 7 — Generate the answer
        python src/generate.py

    The retrieved passages are provided as context to the local LLM.

    The LLM then generates an answer based on the retrieved Mahabharata content.

    🔎 Example

    Question
    Who was Arjuna?
    Retrieval

    The system retrieves passages containing information about:

    Arjuna
    Dhananjaya
    Partha
    Phalguna
    His battles
    His weapons
    His role in the Mahabharata
    Generation

The retrieved context is passed to the LLM to produce a grounded response.

📊 Current Pipeline Statistics

    Component	Result
    Text chunks	5,161
    Embedding dimensions	384
    Vector database	ChromaDB
    Retrieval	Semantic similarity
    LLM	Local
    Paid API	Not required
    🎯 Why RAG?

    A normal LLM:

    Question
    ↓
    LLM
    ↓
    Answer

    can potentially hallucinate information.

This project uses:

Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Mahabharata Context
   ↓
LLM
   ↓
Grounded Answer

This allows the model to answer using the retrieved source material rather than relying entirely on its pretrained knowledge.

🔮 Future Improvements

The current project focuses on the core RAG backend.

Planned improvements:

 FastAPI backend
 REST API for question answering
 React frontend
 Chat-style interface
 Streaming LLM responses
 Source citations
 Retrieval score display
 Conversation history
 Better prompt engineering
 Reranking retrieved documents
 Hybrid keyword + semantic search
 RAG evaluation metrics
 Docker deployment
 Cloud deployment
💡 Future Full-Stack Architecture
                 React Frontend
                       │
                       ▼
                 FastAPI Backend
                       │
                       ▼
                 RAG Pipeline
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
         ChromaDB              Local LLM
             │                   │
             └─────────┬─────────┘
                       ▼
                  Final Answer
                       │
                       ▼
                 React Frontend


📚 Key Concepts Learned

This project demonstrates practical experience with:

Retrieval-Augmented Generation
Natural Language Processing
Text preprocessing
Document chunking
Vector embeddings
Semantic similarity
Vector databases
Information retrieval
Local LLM inference
Hugging Face Transformers
Sentence Transformers
ChromaDB
Python ML pipelines
Git/GitHub


👨‍💻 Author

Barath Babu

B.Tech Computer Science Engineering

GitHub: Barath-co



## Project Status

### Backend RAG Pipeline — Completed

The core RAG retrieval pipeline has been implemented.

It includes:

- Mahabharata text preprocessing
- Text cleaning
- Text chunking
- 384-dimensional embeddings
- ChromaDB vector storage
- Semantic similarity search
- Top-k relevant passage retrieval

### FastAPI Backend — Completed

A FastAPI backend has been added to expose the retrieval pipeline through REST API endpoints.

The backend currently provides:

- `GET /health` — backend health check
- `POST /ask` — retrieves relevant Mahabharata passages
- Swagger API documentation
- CORS configuration for frontend communication

### React Frontend — Completed

A React + TypeScript frontend built with Vite provides the user interface.

The frontend includes:

- Question input
- Retrieval results
- Source passage display
- Section information
- Loading states
- Error handling
- Backend status monitoring
- Conversation history

### Frontend ↔ Backend Integration — Completed

The React frontend successfully communicates with the FastAPI backend.

```text
User Question
      ↓
React Frontend
      ↓
FastAPI /ask
      ↓
Query Embedding
      ↓
ChromaDB Search
      ↓
Relevant Mahabharata Passages
      ↓
FastAPI Response
      ↓
React Frontend


### One important thing

Since your actual repo **doesn't contain the `data/` files anymore**, the README shouldn't imply that someone can clone the repo and immediately run the entire pipeline. That's why I included the note about generated/local data.

Now create the file:

```powershell
code README.md