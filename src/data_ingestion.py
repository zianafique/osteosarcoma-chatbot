import sys

sys.path.append("src")

from pdf_processor import process_all_pdfs
from text_processor import process_text
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


def ingest_data():
    """
    Complete data ingestion pipeline:
    1. Extract text from PDFs
    2. Clean and chunk text
    3. Generate embeddings
    4. Store in vector database
    """

    print("\n" + "=" * 60)
    print("OSTEOSARCOMA RAG - DATA INGESTION PIPELINE")
    print("=" * 60 + "\n")

    # Step 1: Extract PDFs
    print("STEP 1: Extracting text from PDFs...")
    print("-" * 60)
    raw_text = process_all_pdfs()
    print(f"✓ Extracted {len(raw_text):,} characters\n")

    # Step 2: Chunk text
    print("STEP 2: Processing and chunking text...")
    print("-" * 60)
    chunks = process_text(raw_text)
    print(f"✓ Created {len(chunks)} chunks\n")

    # Step 3: Generate embeddings
    print("STEP 3: Generating embeddings...")
    print("-" * 60)
    embedder = EmbeddingGenerator()
    embeddings = embedder.generate_embeddings(chunks)
    print(f"✓ Generated {len(embeddings)} embeddings\n")

    # Step 4: Create vector database
    print("STEP 4: Setting up vector database...")
    print("-" * 60)
    vector_store = VectorStore()
    vector_store.create_collection()
    vector_store.add_documents(chunks, embeddings)
    print()

    # Summary
    print("=" * 60)
    print("DATA INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Total Documents: {len(chunks)}")
    print("Database Location: data/chroma_db/")
    print("Ready for RAG queries!\n")

    return vector_store


if __name__ == "__main__":
    try:
        ingest_data()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
