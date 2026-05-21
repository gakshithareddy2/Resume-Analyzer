import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_FILE = BASE_DIR / "data" / "skills.csv"


def load_skills(skill_file_path=SKILLS_FILE):
    skills = []

    with open(skill_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skills.append(row["skill"].strip())

    return skills


def extract_skills(text, skill_file_path=SKILLS_FILE):
    skills = load_skills(skill_file_path)
    detected_skills = []

    text_lower = text.lower()

    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            detected_skills.append(skill)

    return sorted(list(set(detected_skills)))