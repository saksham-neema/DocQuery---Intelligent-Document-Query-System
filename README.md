code
Markdown
# DocuQuery AI: Intelligent Document Query System

**Our Submission for HackRx 6.0 by Bajaj Finserv**  
**Team:** MindMates

---
<img width="1901" height="884" alt="Screenshot 2025-08-08 222150" src="https://github.com/user-attachments/assets/519bdad2-a6b2-44f4-81a7-4a987986379a" />
<img width="1893" height="886" alt="Screenshot 2025-08-08 222219" src="https://github.com/user-attachments/assets/1298c0ac-a499-4f11-af7d-968b1970d20f" />

## 🚀 Overview

**DocuQuery AI** is an advanced, full-stack application designed to solve a critical business challenge: unlocking the valuable knowledge trapped within large, unstructured documents. We built a powerful system that allows users to "chat" with their documents—from insurance policies to legal contracts—using plain, natural English and receive precise, justified, and structured answers in real-time.

Our solution moves beyond simple keyword searching to true semantic understanding, providing an intuitive, scalable, and automated way to handle document analysis.

### Core Features:
- **On-the-Fly Indexing:** Users can upload documents (via file or URL) and have them instantly added to a searchable knowledge base.
- **Natural Language Queries:** Ask complex questions in plain English, just like you would ask a human expert.
- **Intelligent RAG Pipeline:** Built on a state-of-the-art **Retrieval-Augmented Generation (RAG)** architecture to ensure answers are based *only* on the provided documents, preventing AI hallucinations.
- **Structured JSON Output:** Receive consistent, machine-readable JSON responses with a `decision`, `amount`, and `justification`, perfect for downstream automation.
- **Intuitive Web Interface:** A clean, modern, and responsive frontend makes the entire process seamless and user-friendly.

---

## 🛠️ Tech Stack & Architecture

Our system is engineered with a modern, scalable technology stack, leveraging best-in-class tools for each part of the pipeline.

### Architecture: Retrieval-Augmented Generation (RAG)
Our solution is built around a two-stage RAG pipeline:

1.  **Indexing Pipeline:** When a document is uploaded, it is intelligently parsed by **Docling**, chunked, and then converted into vector embeddings using the **Google Gemini `embedding-001` model**. These vectors are stored in a **ChromaDB** vector database.
2.  **Querying Pipeline:** A user's query is also converted into an embedding. We perform a high-speed similarity search in ChromaDB to retrieve the most relevant text chunks. These chunks, along with the original query, are then "augmented" into a prompt for the **Google Gemini `1.5-flash` model**, which generates the final, reasoned JSON response.

| Component           | Technology                                                                                                | Purpose                                                                                |
| ------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Cloud AI**        | **Google Cloud (Gemini API)**                                                                             | State-of-the-art models for embedding (`embedding-001`) and generation (`gemini-1.5-flash`). |
| **Backend**         | **Python**, **FastAPI**                                                                                   | High-performance, asynchronous API for handling indexing and querying requests.        |
| **Document Parsing**| **Docling**                                                                                               | Advanced, structure-aware parsing of PDFs and other documents.                         |
| **Database**        | **ChromaDB**                                                                                              | High-speed vector database for semantic search and retrieval.                          |
| **Frontend**        | **Vanilla HTML, CSS, JavaScript**                                                                         | A lightweight, responsive, and dependency-free single-page application.                  |
| **Server**          | **Uvicorn**                                                                                               | ASGI server to run the FastAPI application.                                              |

---

## ⚙️ Setup and Installation

Follow these steps to get DocuQuery AI running on your local machine.

### Prerequisites
- Python 3.9+
- An internet connection
- A modern web browser

### Step 1: Clone the Repository

# Replace with your actual repository URL
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Step 2: Install Dependencies
All required Python libraries are listed in requirements.txt.```bash
pip install -r requirements.txt
code
Code
### Step 3: Configure Environment Variables
You will need a Google Gemini API key.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API key to this file:
    ```
    GEMINI_API_KEY=your_actual_api_key_goes_here
    ```
3.  On Windows, you may need to enable Developer Mode for certain libraries to function correctly. See the Windows documentation for how to do this.

### Step 4: Run the Backend Server
Launch the FastAPI server using Uvicorn.

uvicorn main:app --reload

The server will start, typically on http://127.0.0.1:8000. You will see a confirmation message in your terminal that it has connected to ChromaDB.

### Step 5: Launch the Frontend

No build step is required. Simply open the index.html file in your web browser.

## 🚀 Usage

The web interface is designed to be intuitive and guides you through a two-step process:

### 1. Analyze & Index Document:
- Choose to either upload a local PDF file or paste a publicly accessible URL.
- Click the "Analyze & Index" button. The system will process the document in the background.
- Upon completion, a unique Document ID will be generated and displayed. This ID will also be auto-populated in the query section.

### 2. Ask a Question:
- Type your question in plain English into the "Your Query" text area.
- Ensure the correct Document ID is in the field below it (or leave it blank to search all indexed documents).
- Click "Get Answer". The structured JSON response from the AI will appear in the response panel.


## 🎬 YouTube Video
Watch our complete walkthrough and demonstration of DocuQuery AI in action!
▶️ [Watch the YouTube Video](https://youtu.be/ciUSMWbRpK0)
