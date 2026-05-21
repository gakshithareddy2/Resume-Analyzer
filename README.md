# 📄 Automated Resume Analyzer for Job Portals

An AI-powered Resume Analyzer and ATS Candidate Ranking System built using Python, NLP, Streamlit, and spaCy.

The system parses resumes in PDF/DOCX format, extracts candidate information, performs skill analysis, estimates ATS compatibility, and generates structured JSON output for recruiters.

---

# 🚀 Features

- PDF/DOCX Resume Parsing
- Contact Information Extraction
- Resume Section Segmentation
- Skill Extraction using NLP
- Named Entity Recognition (NER)
- ATS Compatibility Scoring
- Candidate Ranking System
- Recruiter Dashboard
- Resume Insights & Suggestions
- JSON Export
- CSV Export

---

# 🛠 Tech Stack

- Python
- Streamlit
- spaCy
- Regex
- pdfminer.six
- python-docx
- pandas
- NLP
- JSON

---

# 📂 Project Structure

Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── sample_resumes/
│   ├── job_description.txt
│   └── skills.csv
│
├── src/
│   ├── parser.py
│   ├── extractors.py
│   ├── cleaner.py
│   ├── segmenter.py
│   ├── matcher.py
│   ├── skill_extractor.py
│   ├── entity_extractor.py
│   ├── contact_extractor.py
│   └── name_extractor.py
│
└── output/
    ├── extracted_text/
    └── sections/

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>
cd Resume-Analyzer