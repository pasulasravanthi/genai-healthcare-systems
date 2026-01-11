def validate_summary(text):
    forbidden_terms = ["mr.", "mrs.", "dob", "date:", "patient id", "name:"]
    required_terms = ["diabetes", "hypertension", "metformin", "lisinopril"]

    issues = []

    for term in forbidden_terms:
        if term in text.lower():
            issues.append(f"Privacy issue: found '{term}'")

    found_required = any(term in text.lower() for term in required_terms)
    if not found_required:
        issues.append("Missing key medical terms")

    return issues

