import re


def extract_email(text):
    """
    Extract email safely even when PDF text is merged.
    Example issue:
    System9398452705Hyderabadg.akshitha.reddy1@gmail.com
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|in|org|net|edu)"
    matches = re.findall(pattern, text)

    if not matches:
        return ""

    email = matches[0]

    # Special fix for merged Gmail emails
    if "@gmail.com" in email:
        before_at = email.split("@")[0]

        # Keep part starting from last lowercase initial pattern like g.akshitha...
        fixed = re.search(r"[a-z](?:[._][a-zA-Z0-9]+)+$", before_at)

        if fixed:
            return fixed.group(0) + "@gmail.com"

    return email


def extract_phone(text):
    match = re.search(r"(\+91[\s-]?)?[6-9]\d{9}", text)
    return match.group(0) if match else ""


def extract_linkedin(text):
    match = re.search(
        r"https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+/?",
        text
    )
    return match.group(0) if match else ""


def extract_github(text):
    match = re.search(
        r"https?://(?:www\.)?github\.com/[a-zA-Z0-9-]+/?",
        text
    )
    return match.group(0) if match else ""


def extract_contact_info(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
    }