import re
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP


def clean_text(text: str) -> str:
    """
    Clean and normalize text

    Args:
        text: Raw text from PDFs

    Returns:
        Cleaned text
    """
    # Remove multiple newlines and replace with single newline
    text = text.replace("\n\n\n", "\n\n")

    # Remove extra spaces (but keep single spaces)
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> List[str]:
    """
    Split text into overlapping chunks

    Args:
        text: Cleaned text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Overlap between adjacent chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        # Get chunk from start to start+chunk_size
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)

        # Move start position, but keep overlap with previous chunk
        start = end - overlap

    return chunks


def process_text(text: str) -> List[str]:
    """
    Complete text processing pipeline:
    1. Clean text
    2. Split into chunks

    Args:
        text: Raw text from PDFs

    Returns:
        List of processed text chunks
    """
    print("Cleaning text...")
    cleaned = clean_text(text)

    print("Chunking text...")
    chunks = chunk_text(cleaned)

    print(f"Created {len(chunks)} text chunks")
    return chunks
