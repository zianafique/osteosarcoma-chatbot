import sys

sys.path.append("src")

from rag_pipeline import RAGPipeline

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("OSTEOSARCOMA RAG CHATBOT - RAG PIPELINE TEST")
    print("=" * 60 + "\n")

    try:
        # Initialize RAG pipeline
        rag = RAGPipeline()

        # Test questions
        test_questions = [
            "What is Osteosarcoma?",
            "What are the symptoms of osteosarcoma?",
            "What is the prognosis of osteosarcoma?",
        ]

        for i, question in enumerate(test_questions, 1):
            print(f"\n{'=' * 60}")
            print(f"QUESTION {i}: {question}")
            print("=" * 60)

            # Get answer from RAG pipeline
            result = rag.query(question)

            print(f"\nANSWER:")
            print("-" * 60)
            print(result["answer"])
            print("-" * 60)

            print(f"\nContext used: {result['context_count']} chunks")
            print(f"Sources:")
            for j, chunk in enumerate(result["context"], 1):
                print(f"  [{j}] {chunk[:100]}...")

        print(f"\n{'=' * 60}")
        print("✓ RAG Pipeline test complete!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
