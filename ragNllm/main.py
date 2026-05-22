
# from fastapi import FastAPI, HTTPException  
# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Dict, Any
# from rag_engine import rag_answer

# app = FastAPI()

# class QueryRequest(BaseModel):
#     query: str
#     role: str

# @app.post("/chat")
# def chat(req: QueryRequest):

#     if not req.query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")

#     if req.role not in ["lawyer", "citizen"]:
#         raise HTTPException(status_code=400, detail="Role must be 'lawyer' or 'citizen'.")

#     return rag_answer(req.query, req.role)



# class CaseRequest(BaseModel):
#     case_facts: str
#     role: str   # "lawyer" or "citizen"

# @app.post("/case_similarity")
# def case_similarity(req: CaseRequest):
#     from rag_engine import analyze_case_similarity
#     results = analyze_case_similarity(req.case_facts, req.role)
#     return {
#         "similar_sections": results
#     }
# # #ollama run mistral
# # #uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from rag_engine import rag_answer, analyze_case_similarity

# -----------------------------
# App Initialization
# -----------------------------

app = FastAPI(
    title="LawBot RAG API",
    description="API for Legal RAG Chatbot",
    version="1.0"
)

# -----------------------------
# Enable CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Models
# -----------------------------

class QueryRequest(BaseModel):
    query: str
    role: str   # "lawyer" or "citizen"


class CaseRequest(BaseModel):
    case_facts: str
    role: str   # "lawyer" or "citizen"


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(req: QueryRequest):

    query = req.query.strip()
    role = req.role.lower()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if role not in ["lawyer", "citizen"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be 'lawyer' or 'citizen'."
        )

    answer = rag_answer(query, role)

    return {
        "query": query,
        "role": role,
        "answer": answer
    }


# -----------------------------
# Case Similarity Endpoint
# -----------------------------

@app.post("/case_similarity")
def case_similarity(req: CaseRequest):

    case_facts = req.case_facts.strip()
    role = req.role.lower()

    if not case_facts:
        raise HTTPException(
            status_code=400,
            detail="Case facts cannot be empty."
        )

    if role not in ["lawyer", "citizen"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be 'lawyer' or 'citizen'."
        )

    results = analyze_case_similarity(case_facts, role)

    return {
        "case_facts": case_facts,
        "role": role,
        "similar_sections": results
    }


# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.get("/")
def health():
    return {
        "status": "LawBot RAG API running"
    }