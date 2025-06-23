 
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to generate LLM response
def generate_answer(query, documents,sources):
    # Prepare context with source tagging
    context = "\n\n".join([f"[Source: {source}]\n{doc}" for source, doc in zip(sources, documents)])

    # Hallucination control prompt
    prompt = f"""
You are a helpful research assistant. Only answer based on the provided context. Do not make up any facts.

Context:
{context}

Question: {query}

Provide the answer as bullet points with citations like this: [Source: doc3.txt]
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()