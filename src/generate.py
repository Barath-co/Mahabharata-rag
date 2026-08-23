from transformers import pipeline


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


print("=" * 60)
print("LOADING LOCAL LANGUAGE MODEL")
print("=" * 60)

print(f"\nModel: {MODEL_NAME}")
print("First run will download the model.\n")


generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=-1
)


print("\nModel loaded successfully!")


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, retrieved_chunks):

    context = ""

    for i, chunk in enumerate(retrieved_chunks):

        context += f"""
SOURCE {i + 1}
SECTION: {chunk['section']}

{chunk['text']}

----------------------------------------
"""


    prompt = f"""
You are a Mahabharata question-answering assistant.

You MUST answer using ONLY the information contained
in the provided Mahabharata sources.

Do NOT use outside knowledge.

Do NOT invent facts.

If the sources do not contain enough information to answer
the question, say:

"I don't have enough information in the retrieved passages
to answer this question."

Answer directly and clearly.

SOURCES:

{context}

QUESTION:

{question}

ANSWER:
"""


    result = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False,
        return_full_text=False
    )


    answer = result[0]["generated_text"].strip()

    return answer


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("LOCAL LLM TEST")
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