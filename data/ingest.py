import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import config

def load_and_chunk_csv(file_path):
    """
    Parses the CSV row-by-row to ensure structural integrity.
    Each product row becomes a single document chunk.
    """
    df = pd.read_csv(file_path)
    documents = []
    
    for _, row in df.iterrows():
        # Build text representation for the vector search
        text_content = (
            f"Product Name: {row.get('product_name', '')}\n"
            f"Brand: {row.get('brand', '')}\n"
            f"Category: {row.get('category', '')} > {row.get('subcategory', '')}\n"
            f"Price: {row.get('price', '')} {row.get('currency', 'INR')}\n"
            f"Discounted Price: {row.get('discounted_price', '')}\n"
            f"Rating: {row.get('rating', '')}/5\n"
            f"Status: {row.get('stock_status', '')}\n"
            f"Description: {row.get('description', '')}"
        )
        
        # Extract structured metadata for potential precise filtering later
        metadata = {
            "product_id": str(row.get("product_id", "")),
            "price": float(row.get("price", 0)) if pd.notnull(row.get("price")) else 0.0,
            "rating": float(row.get("rating", 0)) if pd.notnull(row.get("rating")) else 0.0,
            "stock_status": str(row.get("stock_status", ""))
        }
        
        doc = Document(page_content=text_content, metadata=metadata)
        documents.append(doc)
        
    return documents

def main():
    print("Step 1: Parsing and chunking CSV data...")
    chunks = load_and_chunk_csv(config.CSV_FILE_PATH)
    print(f"Successfully processed {len(chunks)} products.")

    print("\nStep 2: Initializing local Hugging Face embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': config.DEVICE}
    )

    print("\nStep 3: Generating embeddings and storing them in local ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_DB_DIR
    )
    
    print(f"\nSuccess! Your vector database is stored locally at: {config.CHROMA_DB_DIR}")

if __name__ == "__main__":
    main()