import os
import chromadb
from chromadb.config import Settings
from config import CHROMA_PERSIST_DIR


class VectorStore:
    """
    Wrapper around Chroma database for managing embeddings
    """

    def __init__(self):
        """Initialize Chroma persistent database"""
        # Create data directory if it doesn't exist
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

        # Initialize Chroma client (persistent = saves to disk)
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = None

        print(f"✓ Chroma database initialized at: {CHROMA_PERSIST_DIR}")

    def create_collection(self, name: str = "osteosarcoma"):
        """
        Create a new collection (table) in Chroma

        Args:
            name: Name of the collection

        Returns:
            The created collection
        """
        try:
            # Delete if exists (fresh start)
            self.client.delete_collection(name=name)
            print(f"  (Cleared existing collection: {name})")
        except:
            # Collection doesn't exist yet, that's fine
            pass

        # Create new collection
        # metadata={"hnsw:space": "cosine"} means:
        # Use cosine distance for similarity (good for embeddings)
        self.collection = self.client.create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )

        print(f"✓ Collection '{name}' created")
        return self.collection

    def add_documents(self, documents: list, embeddings: list, ids: list = None):
        """
        Add documents and their embeddings to Chroma

        Args:
            documents: List of text chunks
            embeddings: List of embedding vectors
            ids: Optional document IDs (auto-generated if not provided)
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        print(f"Adding {len(documents)} documents to collection...")

        self.collection.add(ids=ids, documents=documents, embeddings=embeddings)

        print(f"✓ {len(documents)} documents added to vector database")

    def search(self, query_embedding: list, n_results: int = 3):
        """
        Search for similar documents using embedding

        Args:
            query_embedding: Embedding of the query
            n_results: Number of results to return

        Returns:
            Search results with documents and distances
        """
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )
        return results

    def get_collection(self, name: str = "osteosarcoma"):
        """
        Get existing collection (load from disk)

        Args:
            name: Name of the collection

        Returns:
            The collection
        """
        self.collection = self.client.get_collection(name=name)
        print(f"✓ Loaded existing collection: {name}")
        return self.collection

    def get_collection_info(self):
        """Get information about the collection"""
        if self.collection:
            count = self.collection.count()
            print(f"Collection contains {count} documents")
            return count
        return 0
