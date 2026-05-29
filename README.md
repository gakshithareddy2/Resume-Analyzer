# 📄 Automated Resume Analyzer for Job Portals

An AI-powered Resume Analyzer and ATS Candidate Ranking System built using **Python, NLP, Streamlit, FastAPI, and spaCy**.

The system automatically parses resumes in **PDF/DOCX** format, extracts structured candidate information, detects technical skills, estimates ATS compatibility, ranks candidates, and generates recruiter-friendly JSON reports.

---

# 🚀 Project Overview

Recruitment teams often receive hundreds of resumes for a single role, making manual screening difficult and time-consuming.

This project automates the initial resume screening process by:

* Extracting resume text
* Segmenting resume sections
* Detecting technical skills
* Performing Named Entity Recognition (NER)
* Calculating ATS compatibility score
* Ranking candidates
* Generating structured JSON output
* Providing recruiter insights and recommendations

The project simulates the **core engine of an Applicant Tracking System (ATS)** used in modern hiring platforms.

---

# ✨ Features

## 📄 Resume Parsing

* PDF Resume Parsing
* DOCX Resume Parsing
* Text Cleaning & Normalization

## 🧠 NLP & Information Extraction

* Candidate Name Extraction
* Contact Information Extraction
* Skill Extraction using NLP
* Named Entity Recognition (NER) using spaCy pre-trained models
* Resume Section Segmentation

## 📊 ATS Analysis

* ATS Compatibility Score
* Matched Skills Detection
* Missing Skills Detection
* Candidate Ranking
* Recruiter Recommendations
* Resume Improvement Suggestions
* Extraction Accuracy Estimation

## 🖥 Dashboard

* Interactive Streamlit Dashboard
* Candidate Ranking Table
* Resume Insights Panel
* JSON Viewer
* CSV Export
* JSON Export

## 🌐 API Support

* FastAPI Wrapper
* Swagger Documentation
* JSON API Response

---

# 🛠 Tech Stack

| Category             | Technologies           |
| -------------------- | ---------------------- |
| Programming Language | Python                 |
| Frontend UI          | Streamlit              |
| Backend API          | FastAPI                |
| NLP Library          | spaCy                  |
| Text Processing      | Regex                  |
| PDF Parsing          | pdfminer.six / PyMuPDF |
| DOCX Parsing         | python-docx            |
| Data Handling        | pandas                 |
| Output Formats       | JSON, CSV              |

---

# 📚 Skill Knowledge Base

The system uses a predefined skill database stored in:

```text
data/skills.csv
```

The CSV file contains technical and soft skills including:

* Python
* Java
* SQL
* Machine Learning
* Deep Learning
* NLP
* HTML/CSS
* FastAPI
* React
* AWS
* Docker
* Git/GitHub
* Power BI
* Communication Skills
* Team Collaboration,etc

The Resume Analyzer compares extracted resume text against this skill ontology to detect candidate skills accurately.

---

# 📂 Project Structure

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
├── screenshots/
│   ├── streamlit_dashboard.png
│   ├── ats_score.png
│   ├── candidate_ranking.png
│   ├── json_output.png
│   └── fastapi_swagger.png
│
└── output/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/gakshithareddy2/Resume-Analyzer.git
cd Resume-Analyzer
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Streamlit Dashboard

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

The Streamlit dashboard allows recruiters to:

* Upload resumes
* Paste job descriptions
* Analyze ATS compatibility
* View matched and missing skills
* Rank candidates
* Download JSON reports

---

# 🌐 Run FastAPI Wrapper

```bash
uvicorn api:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The FastAPI wrapper provides:

* Resume upload endpoint
* JSON response API
* Swagger API testing interface

---

# 📌 API Endpoint

## POST `/parse-resume/`

### Upload:

* PDF Resume
* DOCX Resume

### Returns:

* Structured JSON response

---

# 📦 Example JSON Output

```json
{
  "candidate_name": "John Doe",
  "contact_info": {
    "email": "johndoe@gmail.com",
    "phone": "+91 9876543210"
  },
  "detected_skills": [
    "Python",
    "Machine Learning",
    "SQL"
  ],
  "job_match": {
    "match_percentage": 84.5
  }
}
```

---

# 🧠 ATS Scoring Logic

The ATS score is calculated out of **100**.

| Component           | Max Score |
| ------------------- | --------- |
| Skills Score        | 60        |
| Projects Score      | 20        |
| Education/GPA Score | 10        |
| Experience Score    | 10        |
| Total               | 100       |

---

# 🎯 Extraction Accuracy

The Resume Analyzer was tested on multiple resume formats including:

* ATS-friendly resumes
* STAR-format resumes
* Two-column resumes
* No-heading resumes
* PDF resumes
* DOCX resumes

The extraction accuracy was evaluated by manually comparing extracted fields with original resume content.

The system achieved approximately:

* Contact Information Accuracy: ~95%
* Education Extraction Accuracy: ~90%
* Skill Extraction Accuracy: ~90%
* Project Extraction Accuracy: ~85%

Average overall extraction accuracy:

≈ 90%

---

# 🔍 Resume Section Segmentation

The parser detects:

* Summary
* Education
* Skills
* Projects
* Experience
* Certifications
* Languages

Segmentation is performed using:

* Regex-based extraction
* Keyword heuristics
* Text preprocessing pipeline

---

# 📊 Recruiter Dashboard Features

* ATS Compatibility Estimate
* Candidate Ranking
* Matched Skills
* Missing Skills
* Recruiter Recommendation
* Resume Improvement Insights
* Extraction Accuracy
* Downloadable JSON Reports

---
🔗 Live Project

Streamlit Cloud Link:

https://gakshithareddy2-resume-analyzer-app-qreoy8.streamlit.app/

# ⚠️ Known Limitations

* Highly graphical/image-only resumes may reduce extraction accuracy.
* Some custom resume layouts may require additional parsing rules.
* Multi-column PDF resumes may occasionally affect section ordering.
* ATS score depends on the quality of the provided job description.
* The system currently uses spaCy pre-trained Named Entity Recognition (NER) models and not custom-trained models.

---

# 🎯 Final Outcome

This project demonstrates practical implementation of:

* Natural Language Processing (NLP)
* Resume Parsing
* Information Extraction
* ATS Scoring Systems
* Named Entity Recognition
* Streamlit Application Development
* FastAPI Backend APIs
* Recruiter Workflow Automation

The system successfully automates recruiter-side resume screening and candidate analysis workflows.
