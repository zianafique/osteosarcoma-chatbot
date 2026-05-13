from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class EmbeddingGenerator:
    """
    Generate embeddings using Hugging Face's sentence-transformers
    Model: all-MiniLM-L6-v2 (384-dimensional embeddings)
    """

    def __init__(self):
        """Initialize the embedding model"""
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        print("(This might take a minute on first run, then it's cached)")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        print("✓ Model loaded successfully")

    def generate_embedding(self, text: str):
        """
        Generate embedding for a single text

        Args:
            text: Text to embed

        Returns:
            384-dimensional embedding vector
        """
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def generate_embeddings(self, texts: list):
        """
        Generate embeddings for multiple texts (faster than one-by-one)

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
