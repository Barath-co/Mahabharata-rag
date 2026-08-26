import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

response = client.responses.create(
    model="grok-4.6",
    input="Explain who Arjuna is in one sentence."
)

print(response.output_text)