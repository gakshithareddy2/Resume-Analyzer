def generate_resume_insights(parsed_data):
    skills = parsed_data.get("detected_skills", [])
    sections = parsed_data.get("sections", {})
    job_match = parsed_data.get("job_match", {})

    strengths = []
    issues = []
    suggestions = []

    if len(skills) >= 5:
        strengths.append("Strong technical skill coverage detected.")
    else:
        issues.append("Limited number of technical skills detected.")
        suggestions.append("Add more role-specific technical skills.")

    if sections.get("projects"):
        strengths.append("Project section is available.")
    else:
        issues.append("Projects section is missing or not detected.")
        suggestions.append("Add academic or personal projects with technologies used.")

    if sections.get("experience"):
        strengths.append("Experience section is available.")
    else:
        issues.append("Experience section is missing or not detected.")
        suggestions.append("Add internships, academic work, or team project contributions.")

    if sections.get("education"):
        strengths.append("Education information detected.")
    else:
        issues.append("Education section is missing.")
        suggestions.append("Add degree, university, year, and CGPA/GPA.")

    missing_skills = job_match.get("missing_skills", [])

    for skill in missing_skills[:5]:
        suggestions.append(f"Consider adding or learning {skill} if relevant to the job role.")

    if not strengths:
        strengths.append("Basic resume information was extracted successfully.")

    if not issues:
        issues.append("No major issues detected.")

    return {
        "strengths": strengths,
        "issues": issues,
        "suggestions": suggestions
    }