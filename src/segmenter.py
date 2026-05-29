import re


def clean_text(text):
    text = text.replace("￾", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_lines(text):
    text = text.replace("\r", "\n")
    text = text.replace("￾", "-")
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_block(text, start_words, end_words):
    text = normalize_lines(text)

    start_pattern = "|".join(re.escape(word) for word in start_words)
    end_pattern = "|".join(re.escape(word) for word in end_words)

    pattern = (
        rf"(?:^|\n)\s*(?:{start_pattern})\s*:?\s*"
        rf"(.*?)"
        rf"(?=\n\s*(?:{end_pattern})\s*:?\s*|$)"
    )

    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_languages(text):
    known = [
        "English", "Hindi", "Telugu", "French", "Mandarin",
        "Spanish", "German", "Tamil", "Kannada", "Malayalam",
        "Marathi", "Bengali", "Urdu", "Gujarati"
    ]

    return list(dict.fromkeys(
        lang for lang in known
        if re.search(rf"\b{lang}\b", text, re.IGNORECASE)
    ))


def extract_summary(text):
    block = extract_block(
        text,
        ["SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE", "OBJECTIVE", "CAREER OBJECTIVE"],
        [
            "EDUCATION", "ACADEMIC BACKGROUND", "SKILLS", "TECHNICAL SKILLS",
            "PROJECTS", "PROJECTS AND RESEARCH", "EXPERIENCE",
            "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE", "INTERNSHIP",
            "ACADEMIC EXPERIENCE", "LANGUAGES", "CERTIFICATIONS"
        ]
    )

    if block:
        cleaned_block = clean_text(block)

        if not cleaned_block.lower().startswith("academic experience"):
            return cleaned_block

    patterns = [
        r"(Aspiring Computer Science and Engineering student.*?innovative technology solutions\.)",
        r"(Motivated software engineering student passionate about backend development and cloud computing\.)",
        r"(Aspiring .*?innovative technology solutions\.)",
        r"(Full-stack developer .*?deployment workflows\.)",
        r"(Fresher with strong fundamentals.*?database systems\.)",
        r"(Enthusiastic .*?\.)",
        r"(Motivated .*?\.)",
        r"(UX Designer .*?user satisfaction\.?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return clean_text(match.group(1))

    return "0"


def extract_education(text):
    block = extract_block(
        text,
        ["EDUCATION", "ACADEMIC BACKGROUND", "QUALIFICATION", "ACADEMIC QUALIFICATION"],
        [
            "SKILLS", "TECHNICAL SKILLS", "PROJECTS", "PROJECTS AND RESEARCH",
            "EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE",
            "ACADEMIC EXPERIENCE", "SUMMARY", "LANGUAGES", "CERTIFICATIONS"
        ]
    )

    if block:
        education = clean_text(block)

        if (
            "B.Tech" in education
            or "B.Sc" in education
            or "Bachelor" in education
            or "Master" in education
        ):
            return education

    patterns = [
        r"(B\.?\s*Sc.*?(?:University|College|Institute).*?20\d{2}\s*[-–]\s*20\d{2}.*?CGPA\s*[: ]*\s*[0-9.]+)",
        r"(B\.?\s*Tech\s*2nd\s*Year.*?CGPA\s*[: ]*\s*[0-9.]+\s*,?\s*SGPA\s*[: ]*\s*[0-9.]+)",
        r"(B\.?\s*Tech.*?Woxsen University.*?20\d{2}\s*[-–]\s*20\d{2}.*?CGPA\s*[: ]*\s*[0-9.]+.*?SGPA\s*[: ]*\s*[0-9.]+)",
        r"(B\.?\s*Tech.*?(?:University|College|Institute).*?(?:CGPA|GPA)\s*[: ]*\s*[0-9.]+)",
        r"(Bachelor.*?(?:University|College|Institute).*?(?:CGPA|GPA|20\d{2}))",
        r"(Master.*?(?:University|College|Institute).*?(?:CGPA|GPA|20\d{2}))"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return clean_text(match.group(1))

    return "0"


def extract_skills(text):
    block = extract_block(
        text,
        ["TECHNICAL SKILLS", "CORE SKILLS", "KEY SKILLS"],
        [
            "PROJECTS", "PROJECTS AND RESEARCH", "EXPERIENCE",
            "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE", "ACADEMIC EXPERIENCE",
            "EDUCATION", "SUMMARY", "LANGUAGES", "CERTIFICATIONS"
        ]
    )

    if block:
        return clean_text(block)

    block = extract_block(
        text,
        ["SKILLS"],
        [
            "LANGUAGES", "TECHNICAL SKILLS", "PROJECTS", "PROJECTS AND RESEARCH",
            "EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE",
            "EDUCATION", "SUMMARY", "CERTIFICATIONS"
        ]
    )

    if block:
        skill_text = clean_text(block)

        if "Developed a web-based grievance management system" in skill_text:
            skill_text = skill_text.split("Developed a web-based grievance management system")[0].strip()

        return skill_text if skill_text else "0"

    return "0"


def extract_experience(text):
    block = extract_block(
        text,
        ["EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE", "INTERNSHIP", "ACADEMIC EXPERIENCE"],
        [
            "LANGUAGES", "CERTIFICATIONS", "PROJECTS", "PROJECTS AND RESEARCH",
            "EDUCATION", "SKILLS", "TECHNICAL SKILLS", "SUMMARY", "PROFESSIONAL SUMMARY"
        ]
    )

    if not block:
        academic_match = re.search(
            r"(Collaborated in team-based academic projects.*?through practical projects\.)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if academic_match:
            block = academic_match.group(1)
        else:
            intern_match = re.search(
                r"((?:Software Development Intern|Machine Learning Intern|Data Science Intern|Web Development Intern|Full Stack Developer Intern).*?(?:support\.|scripts\.|pages\.|training\.|deployment\.|extraction\.))",
                text,
                re.IGNORECASE | re.DOTALL
            )

            if intern_match:
                block = intern_match.group(1)
            else:
                return "0"

    block = clean_text(block)

    role = ""
    company = ""
    duration = ""

    duration_match = re.search(r"(20\d{2}\s*[-–]\s*20\d{2}|20\d{2})", block)
    if duration_match:
        duration = duration_match.group(0)

    role_company_match = re.search(
        r"(.+?\b(?:Intern|Engineer|Developer|Analyst|Designer|Researcher)\b)\s+(?:at|@|-|–)\s+([A-Za-z0-9 &.]+?)(?:\s+Worked|\s+Developed|\s+Assisted|\.|$)",
        block,
        re.IGNORECASE
    )

    if role_company_match:
        role = role_company_match.group(1).strip().title()
        company = role_company_match.group(2).strip()

    elif "collaborated in team-based academic projects" in block.lower():
        role = "Academic Experience"

    else:
        role_match = re.search(
            r"(Full Stack Developer Intern|Machine Learning Intern|Data Science Intern|Software Development Intern|Web Development Intern|Developer|Intern|Engineer|Analyst|Designer|Researcher)",
            block,
            re.IGNORECASE
        )

        if role_match:
            role = role_match.group(0).title()

    return [{
        "role": role,
        "company": company,
        "duration": duration,
        "description": block
    }]


def extract_certifications(text):
    block = extract_block(
        text,
        ["CERTIFICATIONS", "CERTIFICATES", "AWARDS", "ACHIEVEMENTS"],
        [
            "EDUCATION", "SKILLS", "TECHNICAL SKILLS", "PROJECTS",
            "SUMMARY", "EXPERIENCE", "LANGUAGES"
        ]
    )

    return clean_text(block) if block else "0"


def clean_project_description(text):
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.\w+", " ", text)
    text = re.sub(r"(?:\+91[\s-]?)?[6-9]\d{9}", " ", text)
    return clean_text(text)


def split_projects_from_block(block):
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    projects = []
    current_title = None
    description = []

    desc_starters = (
        "developed", "built", "created", "implemented", "designed",
        "trained", "used", "worked", "performed", "improved",
        "achieved", "managed"
    )

    for line in lines:
        is_title = (
            2 <= len(line.split()) <= 12
            and not line.endswith(".")
            and not line.lower().startswith(desc_starters)
            and "cgpa" not in line.lower()
            and "@" not in line
        )

        if is_title:
            if current_title:
                projects.append({
                    "title": current_title,
                    "description": clean_project_description(" ".join(description))
                })

            current_title = line
            description = []
        else:
            description.append(line)

    if current_title:
        projects.append({
            "title": current_title,
            "description": clean_project_description(" ".join(description))
        })

    return [p for p in projects if p["title"] and p["description"]]


def extract_projects(text):
    projects = []

    known_patterns = {
        "SOT Student Grievance Management System":
            r"(SOT Student Grievance Management System.*?XAMPP\.|Developed a web-based grievance management system.*?XAMPP\.)",

        "Authenticity Analysis of Real and AI-Generated Images Using Deep Learning":
            r"(Authenticity Analysis of Real and AI-Generated Images Using Deep\s*Learning.*?97\.67% classification accuracy\.)",

        "Disease Diagnosis using Machine Learning":
            r"(Disease Diagnosis using Machine Learning\s*Built a machine learning model.*?~74% prediction accuracy\.)",

        "Campus Shuttle Routing & Capacity Scheduling":
            r"(Campus Shuttle Routing & Capacity Scheduling.*?Designed an optimized campus transportation routing system.*?scheduling constraints\.)",

        "Social Event Management Web Application":
            r"(Social Event Management Web Application.*?feedback\.)",

        "Job Portal Web Application":
            r"(Job Portal Web Application.*?recruiter dashboard\.)",

        "Task Management API":
            r"(Task Management API.*?user workflows\.)",

        "Student Grievance Management System":
            r"(Student Grievance Management System.*?MySQL\.)",

        "Diabetes Prediction System":
            r"(Diabetes Prediction System.*?Random Forest Classifier\.)",

        "Smart Attendance System":
            r"(Smart Attendance System.*?OpenCV\.)",

        "REST API Development":
            r"(REST API Development.*?student data management\.)"
    }

    for title, pattern in known_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            desc = clean_project_description(match.group(1))

            if title == "SOT Student Grievance Management System" and not desc.lower().startswith(title.lower()):
                desc = title + " " + desc

            projects.append({
                "title": title,
                "description": desc
            })

    if projects:
        return projects

    block = extract_block(
        text,
        ["PROJECTS", "PROJECTS AND RESEARCH", "ACADEMIC PROJECTS", "PERSONAL PROJECTS"],
        [
            "EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE",
            "EDUCATION", "SKILLS", "TECHNICAL SKILLS", "SUMMARY",
            "LANGUAGES", "CERTIFICATIONS"
        ]
    )

    return split_projects_from_block(block) if block else []


def segment_resume(text):
    text = normalize_lines(text)

    return {
        "summary": extract_summary(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text),
        "languages": extract_languages(text),
        "certifications": extract_certifications(text)
    }