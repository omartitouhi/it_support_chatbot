from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "How do I fix a DNS error?"}]
)
print(response.choices[0].message.content)