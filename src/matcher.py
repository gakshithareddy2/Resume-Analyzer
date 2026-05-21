import re
from skill_extractor import extract_skills


def calculate_match_score(resume_text, job_description_text):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description_text))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills.difference(resume_skills)

    # 60% weight for skills
    if job_skills:
        skills_score = (len(matched_skills) / len(job_skills)) * 60
    else:
        skills_score = 0

    # 20% weight for projects
    project_keywords = [
        "project",
        "machine learning",
        "web application",
        "dashboard",
        "prediction",
        "classification",
        "deep learning",
        "database",
        "model"
    ]

    resume_lower = resume_text.lower()

    project_matches = [
        keyword for keyword in project_keywords
        if keyword in resume_lower
    ]

    projects_score = min(
        (len(project_matches) / len(project_keywords)) * 20,
        20
    )

    # 10% weight for GPA/CGPA
    education_gpa_score = 0

    gpa_match = re.search(
        r"(?:CGPA|GPA)[:\s]*([0-9.]+)",
        resume_text,
        re.IGNORECASE
    )

    if gpa_match:
        try:
            gpa = float(gpa_match.group(1))

            if gpa >= 8:
                education_gpa_score = 10
            elif gpa >= 7:
                education_gpa_score = 7
            elif gpa >= 6:
                education_gpa_score = 5

        except ValueError:
            education_gpa_score = 0

    # 10% weight for experience
    experience_keywords = [
        "intern",
        "experience",
        "worked",
        "collaborated",
        "developed",
        "implemented"
    ]

    experience_matches = [
        keyword for keyword in experience_keywords
        if keyword in resume_lower
    ]

    experience_score = min(
        (len(experience_matches) / len(experience_keywords)) * 10,
        10
    )

    final_score = (
        skills_score
        + projects_score
        + education_gpa_score
        + experience_score
    )

    return {
        "match_percentage": round(final_score, 2),

        "score_breakdown": {
            "skills_score": round(skills_score, 2),
            "projects_score": round(projects_score, 2),
            "education_gpa_score": round(education_gpa_score, 2),
            "experience_score": round(experience_score, 2)
        },

        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),

        "matched_project_keywords": project_matches,
        "matched_experience_keywords": experience_matches
    }