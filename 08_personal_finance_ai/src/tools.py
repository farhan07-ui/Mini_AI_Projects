import pandas as pd
import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Get the base directory dynamically to avoid path issues in VS Code
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def query_expenses(user_query: str) -> str:
    """Reads the CSV transaction data and returns a structured summary for the LLM."""
    csv_path = os.path.join(CURRENT_DIR, "..", "data", "transactions.csv")
    csv_path = os.path.normpath(csv_path)

    if not os.path.exists(csv_path):
        return "Error: No transaction CSV found. Please upload or add a 'transactions.csv' to the data/ folder."
    
    try:
        df = pd.read_csv(csv_path)
        df.columns = [col.lower().strip() for col in df.columns]
        
        total_spent = 0.0
        if "amount" in df.columns:
            total_spent = df["amount"].sum()
        
        raw_data_summary = df.to_string(index=False)
        return (
            f"--- CSV DATABASE REPORT ---\n"
            f"Total transactions found: {len(df)}\n"
            f"Calculated Total Spending: ${total_spent:,.2f}\n"
            f"All Recorded Transactions:\n"
            f"{raw_data_summary}\n"
            f"---------------------------\n"
        )
    except Exception as e:
        return f"Error processing the CSV data: {str(e)}"


def query_financial_documents(user_query: str) -> str:
    """Loads, vectorizes, and searches local PDFs for relevant context using RAG."""
    pdf_folder = os.path.join(CURRENT_DIR, "..", "data", "statements", "*.pdf")
    pdf_folder = os.path.normpath(pdf_folder)
    pdf_files = glob.glob(pdf_folder)
    
    if not pdf_files:
        return "System Warning: No financial PDF documents (like leases or bank statements) were found in the 'data/statements/' folder to search."
        
    try:
        # 1. Load all PDFs from the folder
        documents = []
        for pdf_path in pdf_files:
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
            
        # 2. Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = text_splitter.split_documents(documents)
        
        # 3. Embed text locally using Ollama
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 4. Spin up an in-memory Chroma Vector Database and index the chunks
        vector_db = Chroma.from_documents(chunks, embeddings)
        
        # 5. Retrieve the top 2 most relevant matches for the query
        results = vector_db.similarity_search(user_query, k=2)
        
        if not results:
            return "No matching entries found in the financial PDF documents."
            
        context = "\n\n".join([f"[From {doc.metadata.get('source', 'Document')} - Page {doc.metadata.get('page', 0) + 1}]:\n{doc.page_content}" for doc in results])
        return f"--- RELEVANT PDF EXCERPTS ---\n{context}\n-----------------------------"
    
    except Exception as e:
        return f"Error analyzing PDF documents: {str(e)}"