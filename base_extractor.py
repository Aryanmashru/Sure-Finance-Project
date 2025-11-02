from PyPDF2 import PdfReader
import pdfplumber


def extract_text_pypdf2(file_path):
    """Extracts text using PyPDF2 for table-like sections."""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_pdfplumber(file_path):
    """Extracts text using pdfplumber for layout-sensitive data."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
