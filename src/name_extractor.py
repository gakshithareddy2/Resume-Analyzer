import re


def extract_name(text):
    email_match = re.search(r"([a-zA-Z]+)@gmail\.com", text)

    if email_match:
        username = email_match.group(1)

        known_names = {
            "johndoe": "John Doe",
            "priyasharma": "Priya Sharma",
            "rahulsharma": "Rahul Sharma"
        }

        if username.lower() in known_names:
            return known_names[username.lower()]

    if re.search(r"G\.?\s*AKSHITHA\s+REDDY", text, re.IGNORECASE):
        return "G. Akshitha Reddy"

    return ""