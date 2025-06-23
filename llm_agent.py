from groq import Groq
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

async def generate_answer(query, context_docs):
    context = "\n\n".join([f"Source {i+1}:\n{doc}" for i, doc in enumerate(context_docs)])
    system_prompt = "You are an AI research assistant. Only answer using the provided context. Do not make up facts."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    response_stream = client.chat.completions.create(
        model="lama-3.3-70b-versatile",
        messages=messages,
        stream=True,
    )

    full_response = ""
    async for chunk in response_stream:
        if chunk.choices[0].delta.get("content"):
            token = chunk.choices[0].delta.content
            full_response += token
            yield token, full_response
            await asyncio.sleep(0.01)
