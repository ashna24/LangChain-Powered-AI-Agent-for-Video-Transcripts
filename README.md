# PitchDeck Auditor AI

An enterprise-grade Retrieval-Augmented Generation (RAG) application that acts as an elite Venture Capitalist to analyze and audit startup pitch decks. 

By utilizing Google's Gemini 2.5 Flash and ChromaDB, this system ingests business proposals (PDFs) and provides hyper-analytical, grounded feedback on market viability, execution risks, and financial logic.

## Technical Architecture
* **Frontend:** Streamlit with custom glassmorphic UI and session state memory for seamless chat history.
* **Orchestration:** LangChain for document chunking, embeddings, and retrieval chains.
* **Vector Database:** ChromaDB for semantic storage of document vectors.
* **LLM & Embeddings:** Google Generative AI (`gemini-2.5-flash` and `gemini-embedding-001`).
* **Document Processing:** PyPDF for local, secure document parsing without relying on external web scrapers.

## Key Features
* **Domain-Specific Persona:** The LLM is strictly constrained via system prompt instructions to adopt an analytical, critical VC persona.
* **Low-Temperature Execution:** Configured for high-fidelity, deterministic responses to prevent hallucination during financial analysis.
* **Optimized State Management:** Utilizes Streamlit's "st.session_state" to cache the vector database and LLM chain, preventing redundant API calls and ensuring instant conversational responses.

##  Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ashna24/LangChain-Powered-AI-Agent-for-Video-Transcripts.git](https://github.com/ashna24/LangChain-Powered-AI-Agent-for-Video-Transcripts.git)
   cd LangChain-Powered-AI-Agent-for-Video-Transcripts
