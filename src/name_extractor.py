import re


def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    ignore = [
        "summary", "education", "skills", "projects", "research",
        "experience", "languages", "contact", "phone", "email",
        "linkedin", "github", "location", "university", "college",
        "institute", "cgpa", "sgpa", "b.tech", "bachelor",
        "technical skills", "professional summary",
        "web technologies", "databases", "machine learning",
        "core concepts", "tools"
    ]

    for line in lines[:100]:
        if "@" in line or "http" in line.lower() or re.search(r"\d", line):
            continue

        clean = re.sub(r"[^A-Za-z. ]", "", line).strip()

        if not clean:
            continue

        if any(word in clean.lower() for word in ignore):
            continue

        words = clean.replace(".", " ").split()

        if 2 <= len(words) <= 4:
            return clean.title()

    return ""