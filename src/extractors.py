import fitz
from docx import Document


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = []

        for page in doc:
            text = page.get_text("text")
            full_text.append(text)

        return "\n".join(full_text).strip()

    except Exception as error:
        return f"Error reading PDF file: {error}"


def extract_text_from_docx(docx_path):
    try:
        document = Document(docx_path)
        full_text = []

        for paragraph in document.paragraphs:
            paragraph_text = paragraph.text.strip()

            if paragraph_text:
                full_text.append(paragraph_text)

        return "\n".join(full_text)

    except Exception as error:
        return f"Error reading DOCX file: {error}"


def extract_text_from_file(file_path):
    file_path = str(file_path)

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    return "Unsupported file format"