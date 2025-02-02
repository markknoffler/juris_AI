import streamlit as st

# Streamlit UI
st.set_page_config(page_title="Simple Chat Interface", layout="wide")
st.title("Simple Chat with Assistant")

# Sidebar for file upload (optional)
with st.sidebar:
    st.header("Upload a Document (Optional)")
    uploaded_file = st.file_uploader("Choose a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question or chat with the assistant..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Simulate assistant response (you can replace this part with actual logic later)
    response_text = f"Assistant response to: {prompt}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.write(response_text)
