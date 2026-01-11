def validate_report(text):
    issues = []

    if "impression" not in text.lower():
        issues.append("Missing Impression section")

    forbidden_terms = ["mr.", "mrs.", "patient name", "date", "dob"]
    for term in forbidden_terms:
        if term in text.lower():
            issues.append(f"Privacy issue: found '{term}'")

    return issues

