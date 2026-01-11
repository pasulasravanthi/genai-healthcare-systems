# ==============================
# 1. VALIDATION FUNCTION
# ==============================
from validation.summary_validation import validate_summary
from evaluation.summary_evaluation import evaluate_summary

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


# ==============================
# 2. IMPORTS
# ==============================

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==============================
# 3. MODEL SETUP
# ==============================

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# ==============================
# 4. LOAD DATA
# ==============================

df = pd.read_csv("data/patient.csv")


# ==============================
# 5. GENERATION PIPELINE
# ==============================

for idx, patient in df.iterrows():
    prompt = f"""
You are a clinical documentation specialist.

Generate a synthetic discharge summary using this format.

Diagnosis:
{patient.diagnosis}

Medications:
{patient.medications}

Outcome:
{patient.outcome}

Now rewrite the above information as a professional discharge summary.
"""

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=120)

    print(f"\n--- Synthetic Patient {idx+1} ---")
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)

    issues = validate_summary(generated_text)
    if issues:
        print("⚠️ Validation issues:")
        for issue in issues:
            print("-", issue)
    else:
        print("✅ Validation passed")

    score, details = evaluate_summary(generated_text)
    print("📊 Evaluation score:", score, "/ 3")
    print("Details:", details)

