# ============================================
# RadExplainAI - Final Stable Version
# ============================================

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ============================================
# 1. RULE-BASED IMPRESSION GENERATOR
# (Safety-critical → NOT delegated to LLM)
# ============================================

def generate_impression(findings_text):
    text = findings_text.lower()

    if "opacity" in text or "pneumonia" in text:
        return "Findings are suspicious for pneumonia."
    if "cardiomegaly" in text:
        return "Mild cardiomegaly without acute pulmonary abnormality."
    if "normal" in text or "clear" in text:
        return "No acute cardiopulmonary abnormality."

    return "Clinical correlation is recommended."


# ============================================
# 2. VALIDATION FUNCTION
# ============================================

def validate_report(text):
    issues = []

    if "impression" not in text.lower():
        issues.append("Missing Impression section")

    forbidden_terms = ["mr.", "mrs.", "patient name", "dob", "date"]
    for term in forbidden_terms:
        if term in text.lower():
            issues.append(f"Privacy issue: found '{term}'")

    return issues


# ============================================
# 3. EVALUATION FUNCTION
# ============================================

def evaluate_report(text):
    score = 0
    details = {}

    details["mentions_findings"] = (
        "cardiac" in text.lower()
        or "lung" in text.lower()
        or "opacity" in text.lower()
    )
    details["has_impression"] = "impression" in text.lower()
    details["length_ok"] = 40 <= len(text) <= 400

    score += int(details["mentions_findings"])
    score += int(details["has_impression"])
    score += int(details["length_ok"])

    return score, details


# ============================================
# 4. MODEL SETUP
# ============================================

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# ============================================
# 5. LOAD FINDINGS DATA
# ============================================

with open("data/findings.txt") as f:
    cases = f.read().split("CASE")


# ============================================
# 6. MAIN PIPELINE
# ============================================

for case in cases:
    if case.strip() == "":
        continue

    # --- LLM USED ONLY FOR REWRITING ---
    prompt = f"""
Rewrite the following chest X-ray findings
using clear, professional radiology language.

Findings:
{case}

Rewritten Findings:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False
    )

    rewritten_findings = tokenizer.decode(
        outputs[0], skip_special_tokens=True
    )

    # --- RULE-BASED IMPRESSION ---
    impression = generate_impression(rewritten_findings)

    final_report = f"""
Findings:
{rewritten_findings}

Impression:
{impression}
"""

    print("\n--- Radiology Report ---")
    print(final_report)

    # --- VALIDATION ---
    issues = validate_report(final_report)
    if issues:
        print("⚠️ Validation issues:")
        for issue in issues:
            print("-", issue)
    else:
        print("✅ Validation passed")

    # --- EVALUATION ---
    score, details = evaluate_report(final_report)
    print("📊 Evaluation score:", score, "/ 3")
    print("Details:", details)

