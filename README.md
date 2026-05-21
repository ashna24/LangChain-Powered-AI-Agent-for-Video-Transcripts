# Auditor AI

This project is an AI tool that acts like a strict startup investor.
# How it works:
- You upload a startup's business plan (a PDF pitch deck).
- The AI quickly reads and memorizes the entire document.
- You can then chat with the AI and ask it to find red flags. Instead of just summarizing the text, the AI actively hunts for unrealistic financial goals, missing market research, and weak business logic.

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

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ashna24/LangChain-Powered-Startup-Auditor.git](https://github.com/ashna24/LangChain-Powered-Startup-Auditor.git)
   cd LangChain-Powered-Startup-Auditor

2. **Install dependencies:**
   ```bash
   pip install streamlit langchain langchain-google-genai langchain-community chromadb pypdf python-dotenv
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```text
   GOOGLE_API_KEY=your_api_key_here
   ```
   *(Note: Ensure your `.env` file is added to your `.gitignore` to keep your credentials secure.)*

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
