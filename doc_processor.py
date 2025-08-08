# doc_processor.py
import time
import google.generativeai as genai
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from docling.datamodel.base_models import DocumentStream
from io import BytesIO

def process_and_store_document(collection, source, document_id: str):
    """
    Loads a document from a source (URL string or binary stream), chunks it,
    embeds it, and stores it in a ChromaDB collection.
    """
    EMBEDDING_MODEL = "models/embedding-001"

    print(f"Processing document: {document_id}")
    
    # --- CHANGE ---
    # Determine if the source is a file stream or a URL string
    if isinstance(source, bytes):
        buf = BytesIO(source)
        docling_source = DocumentStream(name=document_id, stream=buf)
    else:
        docling_source = source # It's a URL string

    # 1. Load and Chunk with Docling
    converter = DocumentConverter()
    doc = converter.convert(docling_source).document
    chunker = HybridChunker()
    chunks = list(chunker.chunk(doc))
    texts_to_embed = [chunk.text for chunk in chunks]
    print(f"Created {len(texts_to_embed)} chunks.")

    # 2. Embed the chunks
    print(f"Embedding {len(texts_to_embed)} chunks...")
    all_embeddings = []
    batch_size = 100
    for i in range(0, len(texts_to_embed), batch_size):
        batch = texts_to_embed[i:i+batch_size]
        response = genai.embed_content(
            model=EMBEDDING_MODEL, content=batch, task_type="retrieval_document"
        )
        all_embeddings.extend(response['embedding'])
        time.sleep(1)

    # 3. Store in ChromaDB
    metadatas = [{"document_id": document_id} for _ in texts_to_embed]
    chunk_ids = [f"{document_id}_{i}" for i in range(len(texts_to_embed))]
    
    collection.add(
        ids=chunk_ids, embeddings=all_embeddings, documents=texts_to_embed, metadatas=metadatas
    )
    print(f"Successfully added {len(texts_to_embed)} chunks for document '{document_id}' to ChromaDB.")
    return len(texts_to_embed)