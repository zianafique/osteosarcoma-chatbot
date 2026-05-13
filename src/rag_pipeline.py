import sys

sys.path.append("src")

from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from groq_client import GroqClient
from config import TOP_K_RESULTS


class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline

    Combines:
    1. Vector database search (retrieve relevant context)
    2. LLM generation (create answer from context)
    """

    def __init__(self):
        """Initialize all components"""
        print("Initializing RAG Pipeline...")
        print("-" * 60)

        # Load embedding model
        self.embedder = EmbeddingGenerator()

        # Load vector database
        print("\nLoading vector database...")
        self.vector_store = VectorStore()
        self.vector_store.get_collection()
        print(f"✓ Loaded {self.vector_store.get_collection_info()} documents")

        # Initialize LLM
        print()
        self.llm = GroqClient()

        print("-" * 60)
        print("✓ RAG Pipeline ready!\n")

    def search_context(self, query: str, n_results: int = None) -> list:
        """
        Search vector database for relevant context

        Args:
            query: User's question
            n_results: Number of results to return (uses TOP_K_RESULTS if None)

        Returns:
            List of relevant text chunks from papers
        """
        if n_results is None:
            n_results = TOP_K_RESULTS

        # Convert question to embedding
        query_embedding = self.embedder.generate_embedding(query)

        # Search vector database
        results = self.vector_store.search(query_embedding, n_results=n_results)

        # Extract just the documents (text chunks)
        context_chunks = results["documents"][0]

        return context_chunks

    def generate_answer(self, query: str, context: list) -> str:
        """
        Generate answer using context and LLM

        Args:
            query: User's question
            context: List of relevant text chunks

        Returns:
            Generated answer from LLM
        """
        # Create prompt with context
        prompt = self.llm.create_prompt(query, context)

        # Send to Groq LLM
        messages = [{"role": "user", "content": prompt}]
        response = self.llm.generate_response(messages)

        return response

    def query(self, question: str) -> dict:
        """
        Complete RAG pipeline: search + generate

        Args:
            question: User's question about Osteosarcoma

        Returns:
            Dictionary with:
            - question: original question
            - answer: generated answer
            - context: source chunks used
            - context_count: number of chunks used
        """
        # Step 1: Search for relevant context
        context = self.search_context(question)

        # Step 2: Generate answer using context
        answer = self.generate_answer(question, context)

        # Step 3: Return complete result
        return {
            "question": question,
            "answer": answer,
            "context": context,
            "context_count": len(context),
        }
