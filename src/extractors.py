from pdfminer.high_level import extract_text
from docx import Document

import pytesseract
from pdf2image import convert_from_path

from PIL import Image


POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_pdf(pdf_path):

    try:
        text = extract_text(pdf_path)

        # OCR fallback if little/no text found
        if len(text.strip()) < 50:

            images = convert_from_path(
                pdf_path,
                poppler_path=POPPLER_PATH
            )

            ocr_text = ""

            for image in images:
                ocr_text += pytesseract.image_to_string(image)

            return ocr_text

        return text

    except Exception as e:
        return f"Error reading PDF with OCR: {e}"


def extract_text_from_docx(docx_path):

    try:
        doc = Document(docx_path)

        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        return "\n".join(full_text)

    except Exception as e:
        return f"Error reading DOCX file: {e}"


def extract_text_from_file(file_path):

    file_path = str(file_path)

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        return "Unsupported file format"