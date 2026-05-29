import re


def extract_email(text):
    text = text.replace("\n", " ")
    text = text.replace("http", " http")

    matches = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|edu|org|net|in|co|io)",
        text,
        re.IGNORECASE
    )

    return matches[0].strip() if matches else ""


def extract_phone(text):
    match = re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}", text)

    if not match:
        return ""

    phone = match.group(0).replace(" ", "").replace("-", "")

    if phone.startswith("+91"):
        number = phone[3:]
    else:
        number = phone

    return f"+91 {number}"


def extract_linkedin(text):
    text = text.replace("￾", "-")
    text = re.sub(r"\s+", "", text)

    match = re.search(
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
        text,
        re.IGNORECASE
    )

    return match.group(0).rstrip("/") if match else ""

def extract_github(text):
    text = text.replace("￾", "")
    text = re.sub(r"\s+", "", text)

    match = re.search(
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+",
        text,
        re.IGNORECASE
    )

    if not match:
        return ""

    github = match.group(0)

    for stop in ["SUMMARY", "EDUCATION", "SKILLS", "PROJECTS", "EXPERIENCE"]:
        if stop.lower() in github.lower():
            github = github[:github.lower().find(stop.lower())]

    return github.rstrip("/")


def extract_location(text):
    known_locations = [
        "Hyderabad", "Telangana", "Bangalore", "Chennai", "Mumbai",
        "Pune", "Delhi", "Ahmedabad", "Gujarat"
    ]

    found = []

    for loc in known_locations:
        if re.search(rf"\b{loc}\b", text, re.IGNORECASE):
            found.append(loc)

    return ", ".join(dict.fromkeys(found))


def extract_contact_info(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "location": extract_location(text)
    }