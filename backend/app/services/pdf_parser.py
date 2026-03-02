import fitz  # PyMuPDF
from typing import List, Dict

def extract_text_from_pdf(file_path: str) -> List[Dict]:
    """
    Extracts text from a PDF file page by page.
    Returns a list of dictionaries containing page number and text.
    """
    doc = fitz.open(file_path)
    extracted_pages = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        # Clean text
        text = " ".join(text.split())
        extracted_pages.append({
            "page_num": page_num + 1,
            "text": text
        })
    
    doc.close()
    return extracted_pages
