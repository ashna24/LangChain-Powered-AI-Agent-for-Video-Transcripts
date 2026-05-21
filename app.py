import sys
import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.documents import Document

load_dotenv()

st.set_page_config(page_title="PitchDeck Auditor AI", page_icon="💼", layout="wide")
st.title("PitchDeck Auditor!")

st.caption("Upload a startup pitch deck or business proposal to audit its market viability, financial logic, and risks.")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', sans-serif;
        background: radial-gradient(circle at top left, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* The Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
 
    .main-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        padding-bottom: 20px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 30px !important;
        backdrop-filter: blur(20px);
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
with st.sidebar:
    st.title("Auditor Dashboard")
    st.markdown("---")
    
    st.info("This system  analyzes business plans for market risks, revenue gaps, and scaling bottlenecks.")

    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type=["pdf"])

if uploaded_file:
    if st.session_state.qa_chain is None:
        data = None
        
    
    with st.status("Analyzing...", expanded=True) as status:
        try:     
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            loader = PyPDFLoader(tmp_file_path)
            data = loader.load()
            
            # Cleaning up the temporary file
            os.remove(tmp_file_path)

        except Exception as e:
            status.update(label ="Error parsing document", state = "error", expanded=True)
            st.error(f"could not read the file. details: {str(e)}")
            st.stop()
            
    if data:
        # Chunking 
        textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text = textSplitter.split_documents(data)

        # Embeddings & storage in Chroma
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001") 
        vector_db = Chroma.from_documents(text, embeddings)

        # Set up Retriever & Retrieval Chain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3, 
            system_instruction="""You are an elite Venture Capitalist and startup auditor. 
            Your job is to thoroughly analyze the provided pitch deck context and evaluate user questions. 
            Be realistic, highly analytical, and critical. Highlight operational risks, market size (TAM) discrepancies, 
            revenue model flaws, and competition gaps based strictly on the document context provided. 
            If data is missing from the pitch deck, call it out explicitly as an investment risk."""
        )

        st.session_state.qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_db.as_retriever())
        status.update(label="Analysis Complete!", state="complete", expanded=False)
if st.session_state.qa_chain is not None:
    st.markdown("💡 **Suggested Audit Queries:**")
    st.code("What are the primary execution risks highlighted in this business plan?")
    st.code("Analyze their revenue strategy. Are there any scaling bottlenecks?")
    st.markdown("---")
    
    st.subheader("💬 Audit Console")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    #capturing new message
    user_query = st.chat_input("Ask a question about business viability, financials, or market size...")

    if user_query:
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
            
        # Query the cached engine
        with st.chat_message("assistant"):
            with st.spinner("Auditing documentation..."):
                response = st.session_state.qa_chain.invoke({"query": user_query})

                safe_response = response["result"].replace("$", "\\$")
                    
                st.write(safe_response)
        st.session_state.chat_history.append({"role": "assistant", "content": response["result"]})
else:
    st.markdown("<br><br><h3 style='text-align: center; color: #64748b;'>Upload a startup pitch deck in the sidebar to run the automated VC risk assessment.</h3>", unsafe_allow_html=True)