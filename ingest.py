from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import shutil

pdf_path = "data/cp.pdf"


if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    print("Make sure the file 'cp.pdf' is inside the 'data' folder.")
    exit()

print(f"✅ Loading {pdf_path}...")

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"✅ Loaded {len(documents)} pages")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,          
    chunk_overlap=300,      
    separators=["\n\n", "\n", ". ", " ", ""],  
    length_function=len
)
docs = text_splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


index_path = "faiss_index"
if os.path.exists(index_path):
    try:
        shutil.rmtree(index_path)
        print("🗑️ Old index deleted")
    except:
        print("⚠️ Could not delete old index. Please delete 'faiss_index' folder manually.")


vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("faiss_index")

print("✅ C++ tutorial PDF indexed successfully!")
print("   You can now run test_tool.py or streamlit run app.py to start your C++ assistant")
