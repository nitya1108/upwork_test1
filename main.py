from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from retriever import load_vector_store, retrieve_context
from llm_agent import generate_answer
from utils import check_cache, save_to_cache, log_to_db
import asyncio

app = FastAPI()

# Load Vector Store
vector_store, doc_titles = load_vector_store()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query = request.query.strip()

    # Check Redis Cache
    cached_response = check_cache(query)
    if cached_response:
        return JSONResponse(content={"cached": True, **cached_response})

    
    top_docs, source_ids = retrieve_context(query, vector_store, doc_titles)

    
    async def response_stream():
        async for chunk, full_response in generate_answer(query, top_docs):
            yield chunk
        save_to_cache(query, {"answer": full_response, "sources": source_ids})
        log_to_db(query, full_response, source_ids)

    return StreamingResponse(response_stream(), media_type="text/plain")
