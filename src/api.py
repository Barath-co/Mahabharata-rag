from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .retrieve import retrieve
from .generate import generate_answer


app = FastAPI(title="Mahabharata RAG API")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ============================================================
# ASK
# ============================================================

@app.post("/ask")
def ask(data: dict):

    question = data.get("question", "").strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    # --------------------------------------------------------
    # 1. RETRIEVE
    # --------------------------------------------------------

    results = retrieve(question, top_k=5)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    sources = []

    for i, document in enumerate(documents):

        metadata = (
            metadatas[i]
            if i < len(metadatas)
            else {}
        )

        sources.append({
            "section": metadata.get(
                "section",
                "Unknown"
            ),
            "text": document
        })

    # --------------------------------------------------------
    # 2. GENERATE
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        sources
    )

    # --------------------------------------------------------
    # 3. RETURN
    # --------------------------------------------------------

    return {
        "answer": answer,
        "sources": sources
    }