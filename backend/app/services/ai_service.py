from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(question: str, transaction_summary: str):

    prompt = f"""
You are a Financial Copilot.

Transaction Data:
{transaction_summary}

Question:
{question}

Rules:
- Give ONLY the final answer.
- Do NOT explain calculations.
- Do NOT show reasoning.
- No step-by-step analysis.
- No bullet points.
- Keep the answer under 15 words.
- Answer like a financial assistant.

Examples:

Q: What is my biggest expense?
A: Food is your biggest expense at ₹500.

Q: How much did I spend in total?
A: You spent ₹500 in total.

Q: Which category has the highest spending?
A: Food has the highest spending at ₹500.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=50
    )

    return response.choices[0].message.content.strip()