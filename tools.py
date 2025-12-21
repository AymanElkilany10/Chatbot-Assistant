# tools.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,               # Fewer, higher-quality matches
        "score_threshold": 0.5  # Lower threshold → catches more relevant but slightly varied phrasing
    }
)


@tool
def search_cpp_tutorial(query: str) -> str:
    """
    Search the C++ tutorial PDF for questions related to C++ programming concepts.
    Covers topics such as variables, data types, loops, conditionals, functions, arrays, structs, and basic syntax.
    Returns relevant explanations or examples from the tutorial.
    """
    docs = retriever.invoke(query)
    content = "\n\n".join([doc.page_content for doc in docs])
    return content if content else "No relevant information found in the C++ tutorial."
