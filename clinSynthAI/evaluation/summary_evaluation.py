def evaluate_summary(text):
    score = 0
    details = {}

    details["mentions_diagnosis"] = (
        "diabetes" in text.lower()
        or "hypertension" in text.lower()
    )
    details["mentions_medications"] = (
        "metformin" in text.lower()
        or "lisinopril" in text.lower()
    )
    details["length_ok"] = 50 <= len(text) <= 400

    score += int(details["mentions_diagnosis"])
    score += int(details["mentions_medications"])
    score += int(details["length_ok"])

    return score, details

