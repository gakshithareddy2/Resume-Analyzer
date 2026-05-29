# 📄 Automated Resume Analyzer for Job Portals

An AI-powered Resume Analyzer and ATS Candidate Ranking System built using Python, Streamlit, FastAPI, spaCy, NLP techniques, and Regular Expressions.

The system automatically parses resumes in PDF and DOCX formats, extracts structured candidate information, identifies technical skills, segments resume sections, matches resumes against job descriptions, calculates ATS compatibility scores, ranks candidates, and generates recruiter-friendly JSON outputs.

---

## 🚀 Live Project

Streamlit Cloud Deployment:

https://gakshithareddy2-resume-analyzer-app-qreoy8.streamlit.app/

---

## 🎯 Project Objective

Recruitment teams often receive hundreds of resumes for a single job posting. Manual screening is time-consuming and inefficient.

This project automates the resume screening process by:

- Parsing PDF and DOCX resumes
- Extracting candidate information
- Identifying technical and soft skills
- Segmenting resume sections
- Matching resumes with job descriptions
- Calculating ATS compatibility scores
- Ranking candidates automatically
- Generating structured JSON outputs
- Providing recruiter recommendations

The project simulates the core functionality of a modern Applicant Tracking System (ATS).

---

## ✨ Features

### Resume Parsing
- PDF Resume Parsing
- DOCX Resume Parsing
- Text Cleaning and Normalization

### Information Extraction
- Candidate Name Extraction
- Email Extraction
- Phone Number Extraction
- LinkedIn Extraction
- GitHub Extraction
- Location Extraction
- Skill Extraction
- Education Extraction
- Experience Extraction
- Project Extraction
- Language Extraction

### Resume Section Segmentation
- Summary
- Education
- Skills
- Experience
- Projects
- Languages
- Certifications

### ATS Analysis
- ATS Compatibility Score
- Matched Skills Detection
- Missing Skills Detection
- Job Description Matching
- Candidate Ranking
- Recruiter Recommendation
- Resume Improvement Suggestions

### Dashboard Features
- Candidate Ranking Dashboard
- ATS Score Visualization
- Recruiter Analysis Panel
- JSON Output Viewer
- Downloadable Reports

### API Support
- FastAPI Backend
- Swagger Documentation
- JSON API Responses

---

## 🛠️ Technology Stack

| Category | Technology |
|-----------|-----------|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend API | FastAPI |
| NLP | spaCy |
| Text Processing | Regex |
| PDF Parsing | PyMuPDF |
| DOCX Parsing | python-docx |
| Data Processing | Pandas |
| Output Format | JSON, CSV |

---

## 📂 Project Structure

```text
Resume-Analyzer/
│
├── app.py
├── api.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sample_resumes/
│   ├── skills.csv
│   └── job_description.txt
│
├── src/
│   ├── parser.py
│   ├── cleaner.py
│   ├── segmenter.py
│   ├── matcher.py
│   ├── skill_extractor.py
│   ├── contact_extractor.py
│   ├── entity_extractor.py
│   └── name_extractor.py
│
├── output/
│   └── testing_results.csv
│
└── notebooks/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/gakshithareddy2/Resume-Analyzer.git
cd Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Streamlit Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 🌐 Run FastAPI

```bash
uvicorn api:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📊 ATS Scoring Logic

The ATS score is calculated out of 100.

| Component | Weight |
|------------|--------|
| Skills Match | 60 |
| Projects Match | 20 |
| Education | 10 |
| Experience | 10 |
| Total | 100 |

---

## 🎯 Extraction Completeness

Extraction Completeness measures how successfully the system extracts information present in the uploaded resume.

Evaluated Sections:

- Candidate Name
- Contact Information
- Skills
- Education
- Experience
- Projects
- Languages

Completeness is displayed in:

- Streamlit Dashboard
- Recruiter Analysis View
- Structured JSON Output

---

## 📁 Testing and Validation

The parser was tested on multiple resume formats:

- ATS Resume
- Full Stack Developer Resume
- Project-Based Resume
- Fresher Resume
- No-Heading Resume
- Two Column Resume
- UX Designer Resume
- PDF Resumes
- DOCX Resumes

Testing results are available in:

```text
output/testing_results.csv
```

---

## 📌 Sample JSON Output

```json
{
  "candidate_name": "John Doe",
  "contact_info": {
    "email": "johndoe@gmail.com",
    "phone": "+91 9876543210"
  },
  "detected_skills": [
    "Python",
    "SQL",
    "Machine Learning"
  ],
  "sections": {
    "education": "...",
    "experience": "...",
    "projects": [...]
  }
}
```

---

## 🎯 Project Deliverables Completed

✅ Resume Parser Engine

✅ PDF and DOCX Support

✅ Resume Section Segmentation

✅ Contact Information Extraction

✅ Skill Extraction

✅ Named Entity Recognition (spaCy)

✅ Structured JSON Output

✅ ATS Compatibility Scoring

✅ Job Description Matching

✅ Candidate Ranking Dashboard

✅ FastAPI Integration

✅ Testing on Multiple Resume Layouts
