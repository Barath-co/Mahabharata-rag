import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "chunks.json"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "embeddings.json"


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# LOAD CHUNKS
# ============================================================

def load_chunks():

    print("Loading chunks...")

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    print(f"Loaded {len(chunks):,} chunks")

    return chunks


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks):

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print(f"Model: {MODEL_NAME}")

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("\nGenerating embeddings...")
    print(f"Texts: {len(texts):,}")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("\nEmbedding generation complete!")

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    return embeddings


# ============================================================
# SAVE
# ============================================================

def save_embeddings(chunks, embeddings):

    print("\nPreparing output...")

    output = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        output.append({
            "chunk_id": chunk["chunk_id"],
            "section": chunk["section"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    print("Saving embeddings...")

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False
        )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("MAHABHARATA EMBEDDING GENERATOR")
    print("=" * 60)

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not INPUT_FILE.exists():

        print("\nERROR: chunks.json not found!")

        print(
            f"Expected:\n{INPUT_FILE}"
        )

        return

    # --------------------------------------------------------
    # Load chunks
    # --------------------------------------------------------

    chunks = load_chunks()

    if not chunks:

        print("\nERROR: No chunks found!")

        return

    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    embeddings = create_embeddings(chunks)

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_embeddings(
        chunks,
        embeddings
    )

    # --------------------------------------------------------
    # Final information
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("DONE!")

    print(
        f"Total embeddings: {len(embeddings):,}"
    )

    print(
        f"Dimensions per embedding: "
        f"{embeddings.shape[1]}"
    )

    print(
        f"Output file:\n{OUTPUT_FILE}"
    )

    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()