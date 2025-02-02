import streamlit as st
import os
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# Constants
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def query_rag(query_text: str):
    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_score(query_text, k=5)

    # Combine context from top results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Use Llama 3 model locally via Ollama
    model = Ollama(model="llama3")  # Change "mistral" to "llama3" if needed
    response_text = model.invoke(prompt)

    # Extract sources from the results
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return formatted_response, response_text, sources


# Streamlit UI
st.set_page_config(page_title="Simple LLM Chat", layout="wide")
st.title("Simple LLM Chat with File Upload")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload a Document")
    uploaded_file = st.file_uploader("Choose a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        with open(os.path.join("data", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Main chat interface
st.header("Chat with the LLM")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question or search for clauses..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate LLM response using query_rag
    try:
        formatted_response, response_text, sources = query_rag(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.write(response_text)
            st.write(f"Sources: {sources}")
    except Exception as e:
        st.error(f"Failed to generate response: {str(e)}")
