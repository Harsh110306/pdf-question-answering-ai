import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="PDF Question Answering System",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF Question Answering System")
st.markdown("Ask questions from your uploaded PDF using AI")

if "document_id" not in st.session_state:
    st.session_state.document_id = None
if "session_id" not in st.session_state:
    st.session_state.session_id = None

st.divider()

uploaded_pdf = st.file_uploader(
    "Upload your PDF file",
    type=["pdf"]
)

if uploaded_pdf and st.button("Process Document"):
    with st.spinner("Processing PDF (Extracting text, chunking, and generating embeddings)..."):
        files = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
        try:
            res = requests.post(f"{API_URL}/documents/upload", files=files)
            if res.status_code == 200:
                data = res.json()
                st.session_state.document_id = data["id"]
                st.success(f"✅ Document '{data['filename']}' processed successfully!")
                
                # Create chat session
                session_res = requests.post(f"{API_URL}/chat/session", json={"document_id": data["id"]})
                if session_res.status_code == 200:
                    st.session_state.session_id = session_res.json()["id"]
            else:
                st.error(f"Error processing document: {res.text}")
        except Exception as e:
            st.error(f"Connection error: Make sure the FastAPI backend is running! ({e})")

if st.session_state.document_id and st.session_state.session_id:
    st.divider()
    st.subheader("Chat with Document")
    
    question = st.text_input(
        "Ask a question from the PDF",
        placeholder="e.g. What is the main topic?"
    )
    
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    res = requests.post(
                        f"{API_URL}/chat/message", 
                        json={"session_id": st.session_state.session_id, "question": question}
                    )
                    if res.status_code == 200:
                        data = res.json()
                        st.subheader("Answer")
                        st.write(data["answer"])
                        
                        if data.get("sources"):
                            with st.expander("Sources Context"):
                                for source in data["sources"]:
                                    sim_score = source.get('similarity_score', 0)
                                    st.markdown(f"**Page {source.get('page_num')}** (Similarity: {sim_score:.4f})")
                                    st.info(source.get("text_snippet"))
                    else:
                        st.error(f"Error getting answer: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
                    
    # Optional features section
    st.divider()
    st.subheader("Advanced Features")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Document Summary"):
            with st.spinner("Generating summary..."):
                try:
                    res = requests.get(f"{API_URL}/documents/{st.session_state.document_id}/summary")
                    if res.status_code == 200:
                        st.info(f"**Summary**: {res.json()['summary']}")
                    else:
                        st.error("Could not generate summary")
                except Exception as e:
                    st.error(f"Error: {e}")
    with col2:
        try:
            res = requests.get(f"{API_URL}/chat/session/{st.session_state.session_id}/download")
            if res.status_code == 200:
                st.download_button(
                    label="Download Chat History as PDF",
                    data=res.content,
                    file_name="chat_history.pdf",
                    mime="application/pdf"
                )
        except:
            pass
else:
    if uploaded_pdf is None:
        st.info("Upload a PDF and click 'Process Document' to start querying.")

st.divider()
st.caption("🔍 AI-Based PDF Question Answering | Python + FastAPI + Streamlit")
