# ingest.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import shutil

# Your English PDF file
pdf_path = "data/cp.pdf"

# Check if file exists
if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    print("Make sure the file 'cp.pdf' is inside the 'data' folder.")
    exit()

print(f"✅ Loading {pdf_path}...")

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"✅ Loaded {len(documents)} pages")

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,          # Slightly smaller → avoids cutting mid-rule
    chunk_overlap=300,       # Enough to keep context across splits
    separators=["\n\n", "\n", ". ", " ", ""],  # Prioritize paragraph breaks
    length_function=len
)
docs = text_splitter.split_documents(documents)

# Best embedding model for English
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Remove old index if exists
index_path = "faiss_index"
if os.path.exists(index_path):
    try:
        shutil.rmtree(index_path)
        print("🗑️ Old index deleted")
    except:
        print("⚠️ Could not delete old index. Please delete 'faiss_index' folder manually.")

# Create new vector store
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")

print("✅ C++ tutorial PDF indexed successfully!")
print("   You can now run test_tool.py or streamlit run app.py to start your C++ assistant")
