import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print("SUCCESS llama-3.1-8b-instant")
except Exception as e:
    print("ERROR llama-3.1-8b-instant:", e)

try:
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print("SUCCESS llama3-8b-8192")
except Exception as e:
    print("ERROR llama3-8b-8192:", e)
