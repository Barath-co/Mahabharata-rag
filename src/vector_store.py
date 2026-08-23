import json
from pathlib import Path
import chromadb


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_FILE = BASE_DIR / "data" / "processed" / "chunks.json"
EMBEDDINGS_FILE = BASE_DIR / "data" / "processed" / "embeddings.json"

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("MAHABHARATA VECTOR DATABASE")
    print("=" * 60)

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not CHUNKS_FILE.exists():
        print("\nERROR: chunks.json not found!")
        print(CHUNKS_FILE)
        return

    if not EMBEDDINGS_FILE.exists():
        print("\nERROR: embeddings.json not found!")
        print(EMBEDDINGS_FILE)
        return

    # --------------------------------------------------------
    # Load chunks
    # --------------------------------------------------------

    print("\nLoading chunks...")

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks):,} chunks")

    # --------------------------------------------------------
    # Load embeddings
    # --------------------------------------------------------

    print("\nLoading embeddings...")

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        embedding_data = json.load(f)

    print(f"Loaded {len(embedding_data):,} embeddings")

    # --------------------------------------------------------
    # Check counts
    # --------------------------------------------------------

    if len(chunks) != len(embedding_data):

        print("\nERROR: Counts do not match!")

        print(f"Chunks:     {len(chunks)}")
        print(f"Embeddings: {len(embedding_data)}")

        return

    # --------------------------------------------------------
    # Create ChromaDB
    # --------------------------------------------------------

    print("\nCreating ChromaDB...")

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name="mahabharata"
    )

    print(
        f"Existing vectors: "
        f"{collection.count():,}"
    )

    # --------------------------------------------------------
    # Prepare data
    # --------------------------------------------------------

    ids = []
    documents = []
    metadatas = []
    vectors = []

    for chunk, embedding_item in zip(
        chunks,
        embedding_data
    ):

        # ----------------------------------------------------
        # Extract actual embedding vector
        # ----------------------------------------------------

        if isinstance(embedding_item, dict):

            embedding = embedding_item["embedding"]

        else:

            embedding = embedding_item

        # ----------------------------------------------------
        # Validate embedding
        # ----------------------------------------------------

        if len(embedding) != 384:

            print(
                "\nERROR: Invalid embedding dimension!"
            )

            print(
                f"Chunk ID: {chunk['chunk_id']}"
            )

            print(
                f"Dimensions: {len(embedding)}"
            )

            return

        # ----------------------------------------------------
        # Add data
        # ----------------------------------------------------

        ids.append(
            str(chunk["chunk_id"])
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "chunk_id": chunk["chunk_id"],
            "section": chunk["section"]
        })

        vectors.append(
            embedding
        )

    # --------------------------------------------------------
    # Insert into ChromaDB
    # --------------------------------------------------------

    print("\nAdding embeddings to ChromaDB...")

    BATCH_SIZE = 500

    for start in range(
        0,
        len(ids),
        BATCH_SIZE
    ):

        end = start + BATCH_SIZE

        collection.upsert(
            ids=ids[start:end],
            embeddings=vectors[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end]
        )

        print(
            f"Added "
            f"{min(end, len(ids)):,} / "
            f"{len(ids):,}"
        )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    count = collection.count()

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)

    print(
        f"Total vectors in ChromaDB: {count:,}"
    )

    print("\nDatabase location:")
    print(CHROMA_DIR)

    print("\nCollection:")
    print(collection.name)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()