import os
from pathlib import Path
from pypdf import PdfReader
from config import PDF_DIR


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a single PDF file

    Args:
        pdf_paths: Path to the PDF file

    Returns:
        Extracted text from all pages
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)

        # Loop through each page
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    # Add page number for reference
                    text += f"\n[Page {page_num + 1}]\n"
                    text += page_text + "\n\n"
            except Exception as e:
                print(
                    f"Warning: Error extracting page {page_num} from {pdf_path}: {str(e)}"
                )

        return text

    except Exception as e:
        print(f"Error: Could not read {pdf_path}: {str(e)}")
        return ""


def process_all_pdfs() -> str:
    """
    Extract text from ALL PDF files in the pdfs/ folder

    Returns:
        Combined text from all PDFs
    """
    all_text = ""

    # Get all PDF files
    pdf_files = sorted(Path(PDF_DIR).glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{PDF_DIR}/' folder!")

    print(f"Found {len(pdf_files)} PDF file(s)")
    print("=" * 60)

    # Process each PDF
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        text = extract_text_from_pdf(str(pdf_file))

        # Add separator between papers
        all_text += f"\n\n{'=' * 60}\n"
        all_text += f"SOURCE: {pdf_file.name}\n"
        all_text += f"{'=' * 60}\n\n"
        all_text += text

    print("=" * 60)
    print(f"Total text extracted: {len(all_text)} characters")
    return all_text
