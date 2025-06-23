from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import get_top_documents
from llm_agent import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        
        top_docs, sources = get_top_documents(request.query)

        
        answer = generate_answer(request.query, top_docs,sources)

        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))