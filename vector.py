import os
import httpx
from dotenv import load_dotenv
from typing import List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from llm import llm_call

# ==========================================================
# ENV + TIKTOKEN CACHE SETUP
# ==========================================================

load_dotenv()

API_ENDPOINT = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

tiktoken_cache_dir = "tiktoken_cache"
os.makedirs(tiktoken_cache_dir, exist_ok=True)

os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

assert os.path.exists(
    os.path.join(
        tiktoken_cache_dir,
        "9b5ad71b2ce5302211f9c61530b329a4922fc6a4"
    )
)

http_client = httpx.Client(verify=False)

# ==========================================================
# 1. DOCUMENT TEXT EXTRACTION
# ==========================================================

def extract_text(file_path: str) -> List[Document]:
    """
    Extract text from multiple document types
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    return documents

# ==========================================================
# 2. CHUNKING WITH CONTEXT PRESERVATION
# ==========================================================

def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Chunk documents without losing semantic context
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    return chunks

# ==========================================================
# 3. CREATE EMBEDDINGS
# ==========================================================

def get_embedding_model() -> OpenAIEmbeddings:
    """
    Initialize embedding model
    """
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        base_url=API_ENDPOINT,
        http_client=http_client
    )
    return embeddings

# ==========================================================
# 4. STORE EMBEDDINGS IN CHROMA DB
# ==========================================================

def store_embeddings(
    documents: List[Document],
    persist_dir: str = "chroma_db"
) -> Chroma:
    """
    Store embeddings into Chroma DB
    """
    embeddings = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectorstore.persist()
    return vectorstore

# ==========================================================
# 5. QUERY CHROMA DB
# ==========================================================

def query_chroma_db(
    query: str,
    persist_dir: str = "chroma_db",
    k: int = 5
) -> List[Document]:
    """
    Query vector database and retrieve relevant chunks
    """
    embeddings = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(query, k=k)
    return results

# ==========================================================
# OPTIONAL: LLM ANSWER GENERATION
# ==========================================================

def generate_answer(query: str, docs: List[Document]) -> str:
    """
    Generate final answer using retrieved context
    """

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
            Answer the question using the context below.

            Context:
            {context}

            Question:
            {query}
        """

    response = llm_call(prompt)
    return response

# ==========================================================
# MAIN FUNCTION
# ==========================================================

def main():
    # ---------------------------------------------
    # STEP 1: Extract text
    # ---------------------------------------------
    # documents = extract_text("TCS_FY25_Financial_Results_Report.pdf")
    # print(f"Extracted {len(documents)} documents with contents: {documents}.")

    # ---------------------------------------------
    # STEP 2: Chunk documents
    # ---------------------------------------------
    # chunks = chunk_documents(documents)
    # print("\n\n📄 Document Chunks:\n")
    # print(chunks)
    # print(f"Total Chunks Created: {len(chunks)}")
    # print("\n")

    # ---------------------------------------------
    # STEP 3 & 4: Store embeddings
    # ---------------------------------------------
    # vectorstore = store_embeddings(chunks)
    # print(f"\n\nEmbeddings stored in Chroma DB: {vectorstore}")
    # print("\n")

    # ---------------------------------------------
    # STEP 5: Query vector DB
    # ---------------------------------------------
    # query = "What are the key financial highlights?"
    query = "What was the net profit for Q4 FY25?"
    retrieved_docs = query_chroma_db(query)
    # print("\n🗂️ Retrieved Documents:\n")
    # print(retrieved_docs)

    # ---------------------------------------------
    # Generate final answer
    # ---------------------------------------------
    answer = generate_answer(query, retrieved_docs)

    # print("\n🔍 Retrieved Context:\n")
    # for doc in retrieved_docs:
    #     print(doc.page_content[:300])
    #     print("-" * 80)

    print("\n🧠 Final Answer:\n")
    print(answer)

# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()
