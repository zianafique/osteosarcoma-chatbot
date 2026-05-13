# Contributing to Osteosarcoma Knowledge Base

## How to Add New Papers

1. Add PDF to `pdfs/` folder
2. Run: `python src/data_ingestion.py`
3. Commit changes: `git add . && git commit -m "Add new paper"`
4. Push: `git push`

## How to Improve the Chatbot

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make changes
4. Test locally: `streamlit run app.py`
5. Push and create a Pull Request

## Code Quality

- Use Python 3.11+
- Follow PEP 8
- Add docstrings to functions
- Test before submitting PR
