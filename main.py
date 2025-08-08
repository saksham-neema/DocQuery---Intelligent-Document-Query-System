# main.py - Final Polished Version
import os
import json
import uuid
from pathlib import Path
import google.generativeai as genai
import chromadb
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, HttpUrl

from doc_processor import process_and_store_document
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration & Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash"
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "bajaj_policy"

app = FastAPI(title="Hybrid RAG API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

try:
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    print(f"Connected to ChromaDB. Collection '{COLLECTION_NAME}' has {collection.count()} items.")
except Exception as e:
    print(f"CRITICAL ERROR connecting to ChromaDB: {e}")
    collection = None

chat_model_client = genai.GenerativeModel(CHAT_MODEL)

# --- Pydantic Models ---
# --- CHANGE: IndexRequest no longer needs document_id ---
class IndexURLRequest(BaseModel):
    document_url: HttpUrl

class QueryRequest(BaseModel):
    user_request: str
    document_id: str | None = None

# --- API Endpoints ---
@app.post("/index-url", summary="Index a new document from a URL")
async def index_document_from_url(request: IndexURLRequest):
    if collection is None: raise HTTPException(status_code=500, detail="Database not available.")
    try:
        # --- CHANGE: Generate a unique document_id on the backend ---
        file_name_base = Path(str(request.document_url).split('?')[0]).stem
        document_id = f"{file_name_base}-{uuid.uuid4().hex[:6]}"
        
        chunk_count = process_and_store_document(collection, str(request.document_url), document_id)
        
        # --- CHANGE: Return the generated document_id ---
        return {
            "message": f"Successfully indexed '{file_name_base}' into {chunk_count} chunks.",
            "document_id": document_id 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index document from URL: {e}")

@app.post("/index-file", summary="Index a new document from an uploaded file")
async def index_document_from_file(file: UploadFile = File(...)): # --- CHANGE: Removed document_id from Form ---
    if collection is None: raise HTTPException(status_code=500, detail="Database not available.")
    try:
        # --- CHANGE: Generate a unique document_id on the backend ---
        file_name_base = Path(file.filename).stem
        document_id = f"{file_name_base}-{uuid.uuid4().hex[:6]}"

        file_content = await file.read()
        chunk_count = process_and_store_document(collection, file_content, document_id)
        
        # --- CHANGE: Return the generated document_id ---
        return {
            "message": f"Successfully indexed file '{file.filename}' into {chunk_count} chunks.",
            "document_id": document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index file: {e}")

@app.post("/query", summary="Query the documents")
async def query_document_endpoint(request: QueryRequest):
    # This endpoint remains the same, no changes needed here.
    if collection is None: raise HTTPException(status_code=500, detail="Database not available.")
    
    query_embedding = genai.embed_content(model=EMBEDDING_MODEL, content=request.user_request, task_type="retrieval_query")['embedding']
    
    where_filter = {"document_id": request.document_id} if request.document_id else {}
    results = collection.query(query_embeddings=[query_embedding], n_results=5, where=where_filter)
    
    retrieved_chunks = results['documents'][0]
    if not retrieved_chunks: return {"decision": "Not Found", "amount": 0, "justification": "Could not find any relevant information in the specified document(s)."}
    
    context_string = "\n\n---\n\n".join(retrieved_chunks)
    prompt_template = f"""You are an expert Insurance Claims Adjudicator. Analyze the user's question based *only* on the provided document excerpts. Your final output must be a single, valid JSON object with "decision", "amount", and "justification" keys. CONTEXT: {context_string} --- USER QUESTION: {request.user_request} --- JSON RESPONSE:"""
    
    response = chat_model_client.generate_content(prompt_template)
    try:
        cleaned_response_str = response.text.strip().replace("```json", "").replace("```", "").strip()
        json_response = json.loads(cleaned_response_str)
        return json_response
    except (json.JSONDecodeError, Exception) as e:
        print(f"Could not parse AI response to JSON: {e}")
        return {"decision": "Error", "amount": 0, "justification": "The AI returned a response that could not be formatted as valid JSON."}