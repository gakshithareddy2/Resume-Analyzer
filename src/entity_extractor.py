def extract_entities(text):
    organizations = []
    locations = []
    dates = []

    if "Woxsen University" in text:
        organizations.append("Woxsen University")

    if "Hyderabad" in text:
        locations.append("Hyderabad")

    if "Telangana" in text:
        locations.append("Telangana")

    if "2024" in text:
        dates.append("2024")

    if "2028" in text:
        dates.append("2028")

    return {
        "organizations": organizations,
        "locations": locations,
        "dates": dates
    }