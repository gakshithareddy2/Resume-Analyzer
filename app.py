# app.py

import streamlit as st
import tempfile
import json
import sys
import time
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from parser import ResumeParser


st.set_page_config(
    page_title="Automated Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


def html(code):
    st.markdown(code, unsafe_allow_html=True)


def clean_section(value, fallback):
    if not value or value == "0" or value == []:
        return fallback
    return value


def format_pills(items, pill_class):
    if not items:
        return "<p class='small'>None detected.</p>"

    return (
        "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;'>"
        + "".join([f"<span class='{pill_class}'>{item}</span>" for item in items])
        + "</div>"
    )


def build_insights(result):
    sections = result["sections"]
    missing_skills = result["missing_skills"]
    score = result["score"]

    insights = []

    if not sections.get("projects"):
        insights.append("Add a Projects section with project title, tools used, and measurable outcome.")

    if sections.get("experience", "0") == "0":
        insights.append("Add internship, work experience, academic work, or team project contribution.")

    if sections.get("education", "0") == "0":
        insights.append("Add degree, university name, graduation year, and CGPA/GPA.")

    if missing_skills:
        insights.append(
            "Improve job match by adding or learning: "
            + ", ".join(missing_skills[:5])
            + "."
        )

    if score >= 70 and not insights:
        insights.append("Resume is well aligned with the job requirements.")

    if not insights:
        insights.append("Resume has good skill coverage, but recruiter review is still recommended.")

    return insights


html("""
<style>
.stApp { background:#f8fafc; color:#0f172a; }
.block-container { padding-top:1rem; max-width:1250px; }

.header {
    background:white;
    border:1px solid #e2e8f0;
    border-radius:18px;
    padding:18px 24px;
    margin-bottom:24px;
    box-shadow:0 8px 22px rgba(15,23,42,.06);
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo { font-size:25px; font-weight:900; }
.nav { color:#64748b; font-weight:600; }

.hero {
    background:linear-gradient(135deg,#ffffff,#eef4ff);
    border:1px solid #dbeafe;
    border-radius:28px;
    padding:34px;
    margin-bottom:24px;
    box-shadow:0 14px 35px rgba(15,23,42,.08);
}

.hero h1 {
    font-size:46px;
    line-height:1.1;
    margin:0;
    color:#0f172a;
}

.hero span { color:#2563eb; }

.hero p {
    color:#64748b;
    font-size:17px;
    margin-top:12px;
}

.card {
    background:white;
    border:1px solid #e2e8f0;
    border-radius:22px;
    padding:24px;
    margin-bottom:20px;
    box-shadow:0 8px 24px rgba(15,23,42,.06);
}

.score-card {
    background:#eff6ff;
    border:1px solid #bfdbfe;
    border-radius:22px;
    padding:28px;
    text-align:center;
    margin-bottom:20px;
}

.score-circle {
    width:145px;
    height:145px;
    border-radius:50%;
    background:conic-gradient(#16a34a var(--score),#e2e8f0 0);
    display:flex;
    align-items:center;
    justify-content:center;
    margin:10px auto;
}

.score-inner {
    width:105px;
    height:105px;
    border-radius:50%;
    background:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    font-weight:900;
}

.skill-pill {
    display:inline-flex;
    align-items:center;
    background:#dbeafe;
    color:#1d4ed8;
    border:1px solid #bfdbfe;
    padding:9px 15px;
    border-radius:999px;
    font-size:13px;
    font-weight:800;
    white-space:nowrap;
}

.missing-pill {
    display:inline-flex;
    align-items:center;
    background:#fee2e2;
    color:#b91c1c;
    border:1px solid #fecaca;
    padding:9px 15px;
    border-radius:999px;
    font-size:13px;
    font-weight:800;
    white-space:nowrap;
}

.good-pill {
    display:inline-block;
    background:#dcfce7;
    color:#15803d;
    padding:7px 13px;
    border-radius:18px;
    font-weight:800;
}

.warn-pill {
    display:inline-block;
    background:#fef3c7;
    color:#b45309;
    padding:7px 13px;
    border-radius:18px;
    font-weight:800;
}

.bad-pill {
    display:inline-block;
    background:#fee2e2;
    color:#b91c1c;
    padding:7px 13px;
    border-radius:18px;
    font-weight:800;
}

.small {
    color:#64748b;
    font-size:14px;
}
</style>
""")


html(
    '<div class="header">'
    '<div class="logo">📄 Resume Analyzer</div>'
    '<div class="nav">Parser Engine · Skill Extraction · spaCy NER · JSON Output · FastAPI Ready</div>'
    '</div>'
)

html(
    '<div class="hero">'
    '<h1>Automated Resume Analyzer<br><span>for Job Portals</span></h1>'
    '<p>Upload resumes, extract structured candidate information, detect skills, estimate ATS compatibility, and generate downloadable recruiter reports.</p>'
    '</div>'
)


uploaded_files = st.file_uploader(
    "📤 Upload Resume Files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

st.markdown("### 📋 Job Description")

job_description = st.text_area(
    "Recruiter can paste the job requirements here",
    placeholder="""
Example:

Looking for a Software Engineer Intern.

Requirements:
• Python
• SQL
• Machine Learning
• NLP
• Git/GitHub
• REST APIs
• Problem Solving
• Team Collaboration
""",
    height=220
)


parser = ResumeParser()
all_results = []


if uploaded_files:

    analysis_steps = [
        "Uploading Resume",
        "Extracting Text",
        "Cleaning Data",
        "Finding Sections",
        "Extracting Contact Details",
        "Detecting Skills",
        "Running spaCy NER",
        "Calculating Compatibility",
        "Generating JSON",
        "Preparing Downloads"
    ]

    st.markdown("## 🔍 Analysis Progress")

    status_box = st.empty()
    progress_bar = st.progress(0)

    for i, step in enumerate(analysis_steps):
        percent = int(((i + 1) / len(analysis_steps)) * 100)
        status_box.info(f"{step} — Step {i + 1} of {len(analysis_steps)}")
        progress_bar.progress(percent)
        time.sleep(0.08)

    with st.spinner("Processing resumes..."):
        for uploaded_file in uploaded_files:
            suffix = Path(uploaded_file.name).suffix

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

            parsed_data, cleaned_text = parser.parse_file(temp_path, job_description)

            contact = parsed_data.get("contact_info", {})
            job_match = parsed_data.get("job_match", {})

            result = {
                "file_name": uploaded_file.name,
                "candidate_name": parsed_data.get("candidate_name", "Unknown"),
                "email": contact.get("email", ""),
                "phone": contact.get("phone", ""),
                "linkedin": contact.get("linkedin", ""),
                "score": job_match.get("match_percentage", 0),
                "matched_skills": job_match.get("matched_skills", []),
                "missing_skills": job_match.get("missing_skills", []),
                "skills": parsed_data.get("detected_skills", []),
                "sections": parsed_data.get("sections", {}),
                "json": parsed_data
            }

            result["insights"] = build_insights(result)
            all_results.append(result)

    status_box.success("✅ Analysis completed successfully!")

    ranked_results = sorted(all_results, key=lambda x: x["score"], reverse=True)

    total = len(ranked_results)
    avg_score = round(sum(r["score"] for r in ranked_results) / total, 2)
    shortlisted = len([r for r in ranked_results if r["score"] >= 70])
    high = len([r for r in ranked_results if r["score"] >= 85])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Candidates", total)

    with c2:
        st.metric("Shortlisted", shortlisted)

    with c3:
        st.metric("Average Compatibility", f"{avg_score}%")

    with c4:
        st.metric("High Compatibility", high)

    st.markdown("## 🏆 Candidate Ranking")

    ranking_df = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": r["candidate_name"],
            "ATS Score": r["score"],
            "Matched Skills": ", ".join(r["matched_skills"]),
            "Missing Skills": ", ".join(r["missing_skills"])
        }
        for i, r in enumerate(ranked_results)
    ])

    st.dataframe(ranking_df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV Report",
        data=ranking_df.to_csv(index=False),
        file_name="candidate_ranking_report.csv",
        mime="text/csv",
        key="download_csv_report"
    )

    st.markdown("## 📌 Recruiter Candidate Analysis Dashboard")

    selected_name = st.selectbox(
        "Select Candidate",
        [r["candidate_name"] for r in ranked_results]
    )

    result = next(r for r in ranked_results if r["candidate_name"] == selected_name)

    score = result["score"]

    projects_value = result["sections"].get("projects", [])
    has_projects = bool(projects_value)
    has_experience = result["sections"].get("experience", "0") != "0"
    has_education = result["sections"].get("education", "0") != "0"

    if score >= 75 and has_projects and has_experience and has_education:
        rating = "Excellent Match"
        badge = "<span class='good-pill'>Recommended</span>"
    elif score >= 50:
        rating = "Good / Review"
        badge = "<span class='warn-pill'>Review Needed</span>"
    else:
        rating = "Low Match"
        badge = "<span class='bad-pill'>Not Recommended</span>"

    left, right = st.columns([1.5, 1])

    with left:
        html("<div class='card'>")

        st.markdown("### 👤 Candidate Profile")
        st.markdown(f"## {result['candidate_name']}")
        html(badge)

        st.write("📧 Email:", result["email"])
        st.write("📞 Phone:", result["phone"])
        st.write("🔗 LinkedIn:", result["linkedin"])

        st.markdown("### 🧠 Skills")
        html(format_pills(result["skills"], "skill-pill"))

        st.markdown("### 💼 Experience")
        experience = clean_section(
            result["sections"].get("experience", ""),
            "Experience section not detected."
        )

        if isinstance(experience, list):
            for exp in experience:
                role = exp.get("role", "")
                company = exp.get("company", "")
                duration = exp.get("duration", "")
                description = exp.get("description", "")

                if role:
                    st.markdown(f"### 💼 {role}")

                if company:
                    st.write(company)

                if duration:
                    st.caption(duration)

                if description:
                    st.write(description)

                st.markdown("---")
        else:
            st.info(experience)

        st.markdown("### 🎓 Education")
        education = clean_section(
            result["sections"].get("education", ""),
            "Education section not detected."
        )
        st.success(education)

        st.markdown("### 🚀 Projects")
        projects = clean_section(
            result["sections"].get("projects", []),
            "Projects section not detected."
        )

        if projects == "Projects section not detected.":
            st.info(projects)
        else:
            with st.expander("View Extracted Projects", expanded=False):
                if isinstance(projects, list):
                    for project in projects:
                        if isinstance(project, dict):
                            title = project.get("title", "")
                            description = project.get("description", "")

                            if title:
                                st.markdown(f"### 📌 {title}")

                            if description:
                                st.write(description)

                            st.markdown("---")
                        else:
                            st.write(str(project))
                else:
                    project_lines = str(projects).replace(". ", ".\n").split("\n")

                    for line in project_lines:
                        if line.strip():
                            st.markdown(f"- {line.strip()}")

        st.markdown("### ✨ Resume Improvement Insights")

        for insight in result["insights"]:
            st.warning(insight)

        html("</div>")

    with right:
        html(
            f"<div class='score-card'>"
            f"<h3>ATS Compatibility Estimate</h3>"
            f"<div class='score-circle' style='--score:{score}%'>"
            f"<div class='score-inner'>{score}%</div>"
            f"</div>"
            f"<h2>{rating}</h2>"
            f"</div>"
        )

        html("<div class='card'>")
        st.markdown("### ✅ Matched Skills")
        html(format_pills(result["matched_skills"], "skill-pill"))
        html("</div>")

        html("<div class='card'>")
        st.markdown("### ❌ Missing Skills")
        html(format_pills(result["missing_skills"], "missing-pill"))
        html("</div>")

        html("<div class='card'>")
        st.markdown("### 🧑‍💼 Recruiter Recommendation")

        if score >= 75 and has_projects and has_experience and has_education:
            st.success("Strongly Recommended")
            st.write("Candidate has strong skill alignment and complete resume sections.")
        elif score >= 50:
            st.warning("Recommended for Recruiter Review")
            st.write("Candidate has relevant skills, but recruiter should review missing sections or missing role-specific skills before shortlisting.")
        else:
            st.error("Low Match")
            st.write("Candidate has limited alignment with the role requirements.")

        html("</div>")

        html("<div class='card'>")
        st.markdown("### 🎯 Extraction Completeness")

        total_fields = 0
        correct_fields = 0

        if result["candidate_name"] and result["candidate_name"] != "Unknown":
            total_fields += 1
            correct_fields += 1

        if result["email"]:
            total_fields += 1
            correct_fields += 1

        if result["phone"]:
            total_fields += 1
            correct_fields += 1

        if result["skills"]:
            total_fields += 1
            correct_fields += 1

        education_section = result["sections"].get("education", "")
        if education_section not in ["0", "", None]:
            total_fields += 1
            correct_fields += 1

        experience_section = result["sections"].get("experience", "")
        if experience_section not in ["0", "", None]:
            total_fields += 1
            correct_fields += 1

        projects_section = result["sections"].get("projects", [])
        if projects_section:
            total_fields += 1
            correct_fields += 1

        completeness = round((correct_fields / total_fields) * 100, 2) if total_fields else 0

        if completeness >= 85:
            st.success(f"Extraction Completeness: {completeness}%")
        elif completeness >= 70:
            st.warning(f"Extraction Completeness: {completeness}%")
        else:
            st.error(f"Extraction Completeness: {completeness}%")

        st.caption(
            "Completeness is calculated only from fields detected in the uploaded resume. "
            "Fields not present in the resume are not counted as extraction failures."
        )

        html("</div>")

        html("<div class='card'>")
        st.markdown("### 📊 Score Breakdown")

        breakdown = result["json"].get("job_match", {}).get("score_breakdown", {})

        st.write(f"Skills Score: {breakdown.get('skills_score', 0)} / 60")
        st.write(f"Projects Score: {breakdown.get('projects_score', 0)} / 20")
        st.write(f"Education/GPA Score: {breakdown.get('education_gpa_score', 0)} / 10")
        st.write(f"Experience Score: {breakdown.get('experience_score', 0)} / 10")

        html("</div>")

        html("<div class='card'>")
        st.markdown("### 📦 Raw JSON Output")

        json_data = json.dumps(result["json"], indent=4)

        with st.expander("View Structured JSON"):
            st.json(result["json"])

        st.download_button(
            label="⬇ Download JSON Report",
            data=json_data,
            file_name=f"{result['candidate_name'].replace(' ', '_')}_report.json",
            mime="application/json",
            key=f"json_download_{result['candidate_name']}_{result['file_name']}"
        )

        html("</div>")

else:
    html(
        "<div class='card'>"
        "<h2>Start Resume Analysis</h2>"
        "<p class='small'>Upload one or more PDF/DOCX resumes to begin analysis.</p>"
        "</div>"
    )