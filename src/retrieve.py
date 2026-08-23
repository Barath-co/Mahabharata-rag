import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"


# ============================================================
# SETTINGS
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded!")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="mahabharata"
)

print("Connected!")

print(
    f"Total documents: {collection.count():,}"
)


# ============================================================
# RETRIEVE
# ============================================================

def retrieve(query, top_k=TOP_K):

    print("\nCreating query embedding...")

    query_embedding = model.encode(
        query
    ).tolist()

    print(
        f"Query embedding dimensions: "
        f"{len(query_embedding)}"
    )

    print("\nSearching ChromaDB...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    return results


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(query, results):

    print("\n" + "=" * 70)
    print("QUERY")
    print("=" * 70)

    print(query)

    print("\n" + "=" * 70)
    print("RETRIEVED CHUNKS")
    print("=" * 70)

    # --------------------------------------------------------
    # Debug: show result keys
    # --------------------------------------------------------

    print("\nResult keys:")

    print(results.keys())

    # --------------------------------------------------------
    # Get results
    # --------------------------------------------------------

    documents = results.get("documents")
    metadatas = results.get("metadatas")
    distances = results.get("distances")

    print("\nDocuments returned:")

    if documents:
        print(len(documents[0]))
    else:
        print("NONE")

    print("\nMetadata returned:")

    if metadatas:
        print(len(metadatas[0]))
    else:
        print("NONE")

    print("\nDistances returned:")

    if distances:
        print(len(distances[0]))
    else:
        print("NONE")

    # --------------------------------------------------------
    # Check documents
    # --------------------------------------------------------

    if not documents or not documents[0]:

        print("\nERROR: No documents were returned!")

        return

    documents = documents[0]

    if metadatas:
        metadatas = metadatas[0]
    else:
        metadatas = [{} for _ in documents]

    if distances:
        distances = distances[0]
    else:
        distances = [None for _ in documents]

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    for i, document in enumerate(documents):

        print("\n" + "-" * 70)

        print(f"RESULT {i + 1}")

        # Metadata

        if i < len(metadatas):

            section = metadatas[i].get(
                "section",
                "Unknown"
            )

            chunk_id = metadatas[i].get(
                "chunk_id",
                "Unknown"
            )

        else:

            section = "Unknown"
            chunk_id = "Unknown"

        print(f"Section: {section}")

        print(f"Chunk ID: {chunk_id}")

        # Distance

        if i < len(distances):

            print(
                f"Distance: {distances[i]:.6f}"
            )

        # Text

        print("\nText:")

        print(document[:1000])

        if len(document) > 1000:

            print("...")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("MAHABHARATA RAG RETRIEVER")
    print("=" * 70)

    print("\nType your question.")

    print("Type 'exit' to stop.")

    while True:

        query = input("\nQuestion: ").strip()

        if query.lower() == "exit":

            print("\nExiting...")

            break

        if not query:

            print(
                "Please enter a question."
            )

            continue

        try:

            results = retrieve(query)

            display_results(
                query,
                results
            )

        except Exception as e:

            print("\nERROR:")
            print(type(e).__name__)
            print(e)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()