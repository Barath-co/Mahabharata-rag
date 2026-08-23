import re
import json
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "mahabharata_clean.txt"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "chunks.json"


# ============================================================
# CHUNK SETTINGS
# ============================================================

CHUNK_SIZE = 700
OVERLAP_WORDS = 100


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_sections(text):
    """
    Extract sections such as:

        SECTION I
        SECTION II
        SECTION XVIII
        SECTION CCII

    The section header does NOT have to start on a new line.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Find SECTION + Roman numeral
    pattern = re.compile(
        r"SECTION\s+([IVXLCDM]+)\b",
        re.IGNORECASE
    )

    matches = list(pattern.finditer(text))

    print(f"Found {len(matches)} section headers")

    sections = []

    for i, match in enumerate(matches):

        section_number = match.group(1).upper()

        start = match.start()

        # End at the beginning of the next section
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        # Remove excessive whitespace
        section_text = re.sub(
            r"\s+",
            " ",
            section_text
        ).strip()

        sections.append({
            "section": f"SECTION {section_number}",
            "text": section_text
        })

    return sections


# ============================================================
# CHUNK CREATION
# ============================================================

def create_chunks(sections):
    """
    Split every section into smaller overlapping chunks.

    Example with CHUNK_SIZE = 700
    and OVERLAP_WORDS = 100:

        Chunk 1 -> words 1 - 700
        Chunk 2 -> words 601 - 1300
        Chunk 3 -> words 1201 - 1900

    Section information is preserved as metadata.
    """

    chunks = []

    chunk_id = 0

    for section in sections:

        section_text = section["text"]

        # Convert section into words
        words = section_text.split()

        start = 0

        while start < len(words):

            # End position of current chunk
            end = start + CHUNK_SIZE

            # Get words for this chunk
            chunk_words = words[start:end]

            # Convert words back into text
            chunk_text = " ".join(chunk_words)

            # ------------------------------------------------
            # Create chunk object
            # ------------------------------------------------

            chunk = {
                "chunk_id": chunk_id,
                "section": section["section"],
                "text": chunk_text
            }

            chunks.append(chunk)

            chunk_id += 1

            # ------------------------------------------------
            # Move forward
            #
            # Example:
            #
            # start = 0
            # chunk size = 700
            # overlap = 100
            #
            # next start = 600
            # ------------------------------------------------

            start += CHUNK_SIZE - OVERLAP_WORDS

    return chunks


# ============================================================
# SAVE CHUNKS
# ============================================================

def save_chunks(chunks):

    # Make sure output directory exists
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save JSON
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("MAHABHARATA CHUNKER")
    print("=" * 60)

    # --------------------------------------------------------
    # Check input file
    # --------------------------------------------------------

    print("\nInput file:")
    print(INPUT_FILE)

    if not INPUT_FILE.exists():

        print("\nERROR: Input file does not exist!")

        print("Expected:")
        print(INPUT_FILE)

        return

    # --------------------------------------------------------
    # Read file
    # --------------------------------------------------------

    print("\nReading Mahabharata...")

    text = INPUT_FILE.read_text(
        encoding="utf-8"
    )

    print(
        f"Characters: {len(text):,}"
    )

    # --------------------------------------------------------
    # Extract sections
    # --------------------------------------------------------

    print("\nExtracting sections...")

    sections = extract_sections(text)

    if not sections:

        print(
            "\nERROR: No sections found."
        )

        # Debug information
        occurrences = list(
            re.finditer(
                r"SECTION",
                text,
                re.IGNORECASE
            )
        )

        print(
            f"Found {len(occurrences)} occurrences "
            "of the word SECTION."
        )

        if occurrences:

            print("\nExample occurrence:")

            pos = occurrences[0].start()

            print(
                text[
                    max(0, pos - 100):
                    pos + 300
                ]
            )

        return

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    print("\nCreating chunks...")

    print(
        f"Chunk size: {CHUNK_SIZE} words"
    )

    print(
        f"Overlap: {OVERLAP_WORDS} words"
    )

    chunks = create_chunks(sections)

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_chunks(chunks)

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print(
        f"Created {len(chunks)} chunks"
    )

    print("\nSaved to:")

    print(OUTPUT_FILE)

    # --------------------------------------------------------
    # Section statistics
    # --------------------------------------------------------

    print("\nSection statistics:")

    section_counts = {}

    for chunk in chunks:

        section = chunk["section"]

        if section not in section_counts:
            section_counts[section] = 0

        section_counts[section] += 1

    for section, count in section_counts.items():

        print(
            f"  {section}: {count} chunks"
        )

    # --------------------------------------------------------
    # First chunks
    # --------------------------------------------------------

    print("\nFirst chunks:")

    for chunk in chunks[:5]:

        word_count = len(
            chunk["text"].split()
        )

        print(
            f"  Chunk {chunk['chunk_id']} | "
            f"{chunk['section']} | "
            f"{word_count} words"
        )

    # --------------------------------------------------------
    # Last chunks
    # --------------------------------------------------------

    print("\nLast chunks:")

    for chunk in chunks[-5:]:

        word_count = len(
            chunk["text"].split()
        )

        print(
            f"  Chunk {chunk['chunk_id']} | "
            f"{chunk['section']} | "
            f"{word_count} words"
        )

    # --------------------------------------------------------
    # Sample chunk
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("SAMPLE CHUNK")
    print("=" * 60)

    if chunks:

        sample = chunks[0]

        print(
            f"\nChunk ID: {sample['chunk_id']}"
        )

        print(
            f"Section: {sample['section']}"
        )

        print(
            f"Words: "
            f"{len(sample['text'].split())}"
        )

        print("\nPreview:\n")

        print(
            sample["text"][:1000]
        )

        print("\n...")

    print("\nDone!")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()