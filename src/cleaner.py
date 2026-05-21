import re


def clean_text(text):

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove repeated special characters
    text = re.sub(r"[•●▪]", " ", text)

    return text.strip()


def clean_section_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()