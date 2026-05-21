import re


def clean_value(text):
    replacements = {
        "inArtificial": "in Artificial",
        "inacademic": "in academic",
        "andalgorithm": "and algorithm",
        "real-worldproblems": "real-world problems",
        "toinnovative": "to innovative",
        "studentcomplaints": "student complaints",
        "PythonWeb": "Python Web",
        "CSSDatabases": "CSS Databases",
        "Basic)Machine": "Basic) Machine",
        "DataPreprocessing": "Data Preprocessing",
        "Using DeepLearning": "Using Deep Learning",
        "usingCNN": "using CNN",
        "evaluatedperformance": "evaluated performance",
        "aweb": "a web",
        "contributing to planning, development, andimplementation": "contributing to planning, development, and implementation",
        "problemsthrough": "problems through"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def segment_resume(text):
    sections = {
        "summary": "",
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "languages": "",
        "certifications": ""
    }

    # Summary
    match = re.search(
        r"(Aspiring Computer Science.*?technology solutions\.)",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        sections["summary"] = clean_value(match.group(1))

    # Education
    match = re.search(
        r"(B\.?Tech.*?SGPA[:\s]*[0-9.]+)",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        sections["education"] = clean_value(match.group(1))

    # Skills
    match = re.search(
        r"(Programming Languages:.*?Jupyter Notebook)",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        sections["skills"] = clean_value(match.group(1))

    # Projects
    start = text.find("Developed a web-based grievance management system")
    end = text.find("Aspiring Computer Science")

    if start != -1 and end != -1 and start < end:
        project_text = text[start:end]

        project_text = re.sub(
            r"9398452705.*?Technical Skills",
            "",
            project_text,
            flags=re.IGNORECASE | re.DOTALL
        )
        project_text = re.sub(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "",
            project_text
        )
        project_text = re.sub(r"https?://\S+", "", project_text)
        project_text = re.sub(
            r"English Telugu Hindi",
            "",
            project_text,
            flags=re.IGNORECASE
        )
        project_text = re.sub(
            r"Languages",
            "",
            project_text,
            flags=re.IGNORECASE
        )

        sections["projects"] = clean_value(project_text)

    # Experience
    match = re.search(
        r"(Collaborated in team-based academic projects.*?practical projects\.)",
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        sections["experience"] = clean_value(match.group(1))

    # Languages
    if re.search(r"English\s*Telugu\s*Hindi", text, re.IGNORECASE):
        sections["languages"] = "English, Telugu, Hindi"

    # Final cleanup: if section not detected, store as "0"
    for key in sections:
        if not sections[key]:
            sections[key] = "0"
        else:
            sections[key] = clean_value(sections[key])

    return sections