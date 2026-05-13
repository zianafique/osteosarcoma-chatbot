# 🦴 Osteosarcoma Knowledge Base Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot powered by peer-reviewed research papers on Osteosarcoma (bone cancer).

## 🎯 Overview

This chatbot answers questions about Osteosarcoma by:
1. **Retrieving** relevant chunks from a vector database of research papers
2. **Augmenting** the query with context from scientific literature
3. **Generating** accurate answers using Groq's Llama 3.1 LLM

All answers are based **only** on the provided research papers - no hallucinations!

## 📊 Project Statistics

- **Papers**: 5 peer-reviewed research papers on Osteosarcoma
- **Text Extracted**: 224,587 characters
- **Chunks Created**: 276 semantic chunks
- **Vector Database**: Chroma (locally stored)
- **Embedding Model**: Hugging Face all-MiniLM-L6-v2 (384D vectors)
- **LLM**: Groq Llama 3.1 70B (completely free)

## 🏗️ Architecture
PDF Papers → Text Extraction → Chunking → Embeddings → Vector DB
↓
Semantic Search
↓
User Question → Embedding → Vector DB Search → Context Retrieval
↓
Groq LLM (with context)
↓
User Answer

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Windows/Mac/Linux

### Installation

1. **Clone/Download this repository**

2. **Create virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   - Create `.env` file in project root
   - Add: `GROQ_API_KEY=your_api_key_here`
   - Get free key at: https://console.groq.com

5. **Prepare data** (first time only)
```bash
   python src/data_ingestion.py
```
   This processes PDFs and creates vector database (~5 minutes first run)

6. **Run the app**
```bash
   streamlit run app.py
```
   Opens at: http://localhost:8501

## 📁 Project Structure
osteosarcoma-chatbot/
├── pdfs/                          # Your research papers (5 PDFs)
├── data/
│   └── chroma_db/                # Vector database (created by data_ingestion.py)
├── src/
│   ├── config.py                 # Configuration (API keys, constants)
│   ├── pdf_processor.py          # PDF text extraction
│   ├── text_processor.py         # Text cleaning and chunking
│   ├── embeddings.py             # Embedding generation
│   ├── vector_store.py           # Chroma database management
│   ├── groq_client.py            # Groq LLM integration
│   └── rag_pipeline.py           # RAG logic (search + generate)
├── app.py                        # Streamlit web interface
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not in GitHub!)
├── .gitignore                    # Git ignore rules
└── README.md                     # This file


## 🔬 How It Works

### Data Ingestion Pipeline
1. **PDF Extraction**: PyPDF reads your research papers
2. **Text Cleaning**: Removes formatting artifacts
3. **Chunking**: Splits into 1000-char chunks with 200-char overlap
4. **Embeddings**: Converts to 384-dimensional semantic vectors
5. **Storage**: Stores in local Chroma vector database

### Query Pipeline
1. User asks: "What is osteosarcoma?"
2. Question converted to embedding
3. Vector DB searches for 3 most similar chunks
4. Chunks + question sent to Groq LLM
5. LLM generates answer based only on context
6. Answer displayed with source chunks

## 💡 Key Features

✅ **No Hallucinations**: Answers only from research papers  
✅ **Fast**: Local vector search + Groq's fast inference  
✅ **Transparent**: Show source chunks for every answer  
✅ **Free**: No costs (Groq free tier, local vector DB)  
✅ **Easy to Deploy**: Works on any cloud platform  
✅ **Scalable**: Add more PDFs, they auto-ingest  

## 🎓 Technical Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Vector DB | Chroma | Local, fast, free |
| Embeddings | Hugging Face | Free, accurate, open-source |
| LLM | Groq Llama 3.1 70B | Fast, powerful, completely free |
| Web UI | Streamlit | Simple, Python-only, professional |
| PDF Processing | PyPDF | Simple, open-source |

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap for context
TOP_K_RESULTS = 3  # Chunks to retrieve per query
GROQ_MODEL = "llama-3.1-70b-versatile"  # LLM model
```

## 📝 Usage Examples

**Question 1: Definition**
Q: What is Osteosarcoma?
A: Osteosarcoma is the most common primary malignant bone tumor
that typically affects adolescents and young adults...

**Question 2: Clinical Information**
Q: What are the symptoms?
A: Common symptoms include localized bone pain, swelling,
redness, and warmth at the tumor site...

**Question 3: Statistics**
Q: What is the 5-year survival rate?
A: The 5-year relative survival for osteosarcoma cases
in children aged 0-9 was 71.8%...


## 🚀 Deployment

### Option 1: Hugging Face Spaces (Easiest)
1. Create account at huggingface.co
2. Create new Space (Streamlit)
3. Upload: `requirements.txt`, `app.py`, `src/`, `pdfs/`
4. Create Secret: `GROQ_API_KEY`
5. Deployed! Get public URL

### Option 2: Railway.app
1. Connect GitHub repo
2. Add `GROQ_API_KEY` environment variable
3. Railway auto-deploys

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

## 📚 Papers Included

1. **ML_Bone_osteosarcoma_tumor_classification.pdf**
   - Machine learning approaches for OS classification

2. **DL_A deep learning study on osteosarcoma detection from histological images.pdf**
   - Deep learning for OS detection

3. **Cancer - 2022 - Cole - Osteosarcoma A Surveillance Epidemiology and End Results program‐based analysis from 1975 to 2017.pdf**
   - Epidemiological analysis and survival statistics

4. **DL_Development_of_the_Osteosarcoma_Lung_Nodules_Detection_Model.pdf**
   - Lung nodule detection using deep learning

5. **ML_Application of interpretable machine learning algorithms to predict distant metastasis in osteosarcoma.pdf**
   - ML for metastasis prediction

## 🛠️ Troubleshooting

**Q: "No PDFs found in pdfs/ folder"**
- A: Place your PDF files in the `pdfs/` folder

**Q: "GROQ_API_KEY not found"**
- A: Create `.env` file with `GROQ_API_KEY=your_key`

**Q: Slow first run**
- A: First run downloads the embedding model (~300MB), then cached

**Q: "Error calling Groq API"**
- A: Check API key is valid at console.groq.com

## 📊 Performance Metrics

- **PDF Extraction**: ~2 seconds for 5 papers
- **Embedding Generation**: ~1 minute for 276 chunks (first run only)
- **Query Response Time**: ~2-3 seconds (search + LLM)
- **Model Loading**: ~10 seconds (one-time at startup)

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Conversation memory (context from previous questions)
- [ ] PDF upload feature
- [ ] Citation tracking with page numbers
- [ ] Answer confidence scores
- [ ] Similar questions recommendations
- [ ] Fine-tuned embeddings for medical domain

## 📖 Learning Outcomes

This project demonstrates:
- ✅ RAG (Retrieval-Augmented Generation) architecture
- ✅ Vector databases and semantic search
- ✅ LLM integration and API usage
- ✅ Text processing and NLP pipelines
- ✅ Building production-ready Python applications
- ✅ Web UI development with Streamlit
- ✅ Free and open-source tools usage

Perfect for portfolios and AI engineer job applications!

## 📄 License

Open source - feel free to use, modify, and learn!

## 👤 Author

Built as a portfolio project showcasing RAG, Vector Databases, and LLM integration.

## 🤝 Contributing

Have suggestions? Found bugs? Feel free to improve!

## 📞 Support

For questions about the project, check:
- Documentation in `README.md`
- Code comments in `src/` files
- Streamlit sidebar for feature info

---

**Happy chatting! 🦴**