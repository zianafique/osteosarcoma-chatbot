import sys

sys.path.append("src")

from pdf_processor import process_all_pdfs
from text_processor import process_text

if __name__ == "__main__":
    print("Starting PDF extraction...")
    print()

    try:
        text = process_all_pdfs()
        print()
        print(f"\nSUCCESS! Extracted {len(text):,} characters")
        print("\nFirst 500 characters of extracted text:")
        print("-" * 60)
        print(text[:500])
        print("-" * 60)

        # Now test chunking
        print("\n\nNow testing text chunking...")
        print()

        chunks = process_text(text)

        print()
        print(f"Number of chunks created: {len(chunks)}")
        print(
            f"Average chunk size: {sum(len(c) for c in chunks) // len(chunks)} characters"
        )
        print()
        print("First chunk (sample):")
        print("-" * 60)
        print(chunks[0][:300] + "...")
        print("-" * 60)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
