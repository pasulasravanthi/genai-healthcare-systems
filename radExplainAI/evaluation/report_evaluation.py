def evaluate_report(text):
    score = 0
    details = {}

    details["mentions_findings"] = (
        "cardio" in text.lower()
        or "lung" in text.lower()
        or "opacity" in text.lower()
    )
    details["has_impression"] = "impression" in text.lower()
    details["length_ok"] = 40 <= len(text) <= 300

    score += int(details["mentions_findings"])
    score += int(details["has_impression"])
    score += int(details["length_ok"])

    return score, details

