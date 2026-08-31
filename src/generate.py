
import os
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Make sure it is present in your .env file."
    )


client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


print("=" * 60)
print("LOADING GEMINI LANGUAGE MODEL")
print("=" * 60)

print(f"\nModel: {MODEL_NAME}")
print("Using Gemini API...\n")

print("Gemini client initialized successfully!")


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, retrieved_chunks):

    context = ""

    for i, chunk in enumerate(retrieved_chunks):

        context += f"""
SOURCE {i + 1}
SECTION: {chunk.get('section', 'Unknown')}

{chunk.get('text', '')}

----------------------------------------
"""


    prompt = f"""
You are a Mahabharata question-answering assistant.

Your job is to answer the user's question using ONLY
the retrieved Mahabharata passages provided below.

IMPORTANT RULES:

1. Use ONLY information supported by the retrieved passages.

2. Do NOT use your own knowledge of the Mahabharata to
   fill in missing information.

3. Do NOT invent facts, names, events, relationships,
   dates, locations, or interpretations.

4. Before answering, compare the retrieved passages and
   check whether they actually contain enough evidence
   to answer the question.

5. If multiple passages provide information about the
   same event or person, combine them carefully.

6. If the question asks about a sequence of events,
   explain the events step-by-step and preferably in
   chronological order.

7. If the retrieved passages do not contain enough
   information, respond exactly with:

"I don't have enough information in the retrieved
passages to answer this question."

8. Keep the answer clear and reasonably concise.

9. At the end, provide the sections used to answer the
   question.

RETRIEVED MAHABHARATA PASSAGES:

{context}

USER QUESTION:

{question}

ANSWER:
"""


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )


    answer = response.text.strip()

    return answer


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("GEMINI RAG GENERATION TEST")
    print("=" * 60)


    test_question = "Who was Arjuna?"


    test_chunks = [
        {
            "section": "SECTION XLIX",
            "text": """
The Pandavas of immeasurable energy have been filled
with rage. I have heard how Arjuna hath gratified in
battle by means of his bow the god of gods. The Lokapala
showed themselves unto Phalguna in order to give away
their weapons unto that bull of the Kuru race.
"""
        },
        {
            "section": "SECTION XXXVIII",
            "text": """
Janamejaya said that he desired to hear the history of
the acquisition of weapons by Arjuna of spotless deeds.
He also called Arjuna Dhananjaya and described him as
possessing mighty arms and great energy.
"""
        }
    ]


    print(f"\nQuestion: {test_question}")
    print("\nGenerating answer...\n")


    answer = generate_answer(
        test_question,
        test_chunks
    )


    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)

    print("\nDone!")

