import os
import tempfile
import streamlit as st
from embedchain import App 

# COnfiguring the embedchain app
def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"api_key": api_key}},
            "vectordb": {"prvoider": "chroma", "config": {"dir": db_path}},
            "embedder": { "provider": "openai", "config": {"api_key": api_key}},
        }
    )
    
    # Setting up the streamlit App
st.title("NObray, a seamless chat with your PDF")

openai_access_token = st.text_input("OpenAI API Key", type="password")

# Initialize embedchain App
if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token)
    
# Upload a pdf file
pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

# Add the pdf file to the knowledge base
if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(pdf_file.getvalue())
        app.add(f.name, data_type="pdf_file")
    os.remove(f.name)
    st.success(f"Added {pdf_file.name} to knowledge base!")
    
# Ask questios abot the PDF

prompt = st.text_input("Ask a question about the PDF")

# Display answer
if prompt:
    answer = app.chat(prompt)
    st.write(answer)