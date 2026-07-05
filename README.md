# PDF Chatbot with RAG

An AI-powered chatbot that reads your PDF documents and lets you ask questions, generate summaries, create flashcards, quizzes, and more — all using Retrieval-Augmented Generation (RAG).

---

## What It Does

| Feature | Description |
|---------|-------------|
| **AI Chat** | Ask questions about your PDF and get accurate answers |
| **Summarize** | Generate brief, detailed, or chapter-by-chapter summaries |
| **Flashcards** | Create study flashcards from your document |
| **Quiz** | Generate multiple choice, true/false, or short answer quizzes |
| **Interview Prep** | Get AI-generated interview questions from your PDF |
| **Semantic Search** | Search through your document using meaning, not just keywords |
| **Notes** | Take and save notes from your analysis |
| **Analytics** | View statistics about your document and embeddings |
| **Vector DB Inspector** | Browse the stored vector database records |

---

## How It Works

```
Your PDF → Split into chunks → Convert to embeddings → Store in ChromaDB
                                                         ↓
User asks question → Find similar chunks → Send to LLM → Get answer
```

1. **Upload a PDF** — The app reads and splits it into small chunks
2. **Create Embeddings** — Each chunk is converted to a vector (list of numbers) that captures its meaning
3. **Store in Vector DB** — Embeddings are stored in ChromaDB for fast searching
4. **Ask Questions** — Your question is converted to a vector, similar chunks are found, and the LLM generates an answer based on those chunks

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web Interface | Streamlit |
| LLM | Groq (Llama 3.3 70B) |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| PDF Reading | PyPDF2 |
| Charts | Plotly |

---

## Prerequisites

- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com/keys)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/pdf-chatbot-rag.git
cd pdf-chatbot-rag
```

**2. Create a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up your API key**

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

**5. Run the app**

```bash
streamlit run Home.py
```

The app opens at `http://localhost:8501`

---

## Project Structure

```
pdf-chatbot-rag/
├── Home.py                 # Main page - upload PDFs
├── pages/
│   ├── 01_chat.py          # AI chat with your PDF
│   ├── 02_summary.py       # Generate summaries
│   ├── 03_notes.py         # Take notes
│   ├── 04_flashcards.py    # Create flashcards
│   ├── 05_quiz.py          # Generate quizzes
│   ├── 06_interview.py     # Interview question prep
│   ├── 07_search.py        # Semantic search
│   ├── 08_embeddings.py    # Embedding info
│   ├── 09_vector_db.py     # Vector DB inspector
│   ├── 10_analytics.py     # Document analytics
│   ├── 11_settings.py      # App settings
│   ├── 12_rag_config.py    # RAG pipeline config
│   └── 13_current_config.py # View current settings
├── components/
│   ├── navigation.py       # Sidebar navigation
│   ├── styles.py           # Custom CSS styles
│   ├── charts.py           # Plotly chart components
│   ├── cards.py            # Metric card components
│   └── session.py          # Session state management
├── utils/
│   ├── pdf_reader.py       # PDF text extraction
│   ├── chunking.py         # Text chunking
│   ├── embeddings.py       # Embedding generation
│   ├── vector_db.py        # ChromaDB operations
│   ├── retriever.py        # Semantic search
│   ├── prompt_builder.py   # LLM prompt construction
│   └── gemini_llm.py       # Groq LLM interface
├── config.py               # App configuration
├── .env                    # API keys (not committed)
└── requirements.txt        # Python dependencies
```

---

## Configuration

You can adjust settings from the **Settings** and **RAG Config** pages in the app:

| Setting | Default | Description |
|---------|---------|-------------|
| Chunk Size | 500 | Characters per text chunk |
| Chunk Overlap | 100 | Overlap between chunks |
| Top-K Results | 3 | Number of chunks retrieved per query |
| LLM Model | llama-3.3-70b-versatile | Groq model for answers |
| Embedding Model | all-MiniLM-L6-v2 | Model for vector embeddings |

---

## License

MIT License. See [LICENSE](LICENSE) for details.
