# 🏥 GenAI Healthcare Systems

This repository contains two production-style Generative AI systems
designed for healthcare applications with a strong focus on
**safety, validation, and explainability**.

---

## 📌 Projects Overview

### 1️⃣ ClinSynthAI — Synthetic Clinical Discharge Summaries

ClinSynthAI generates **privacy-safe synthetic discharge summaries**
from structured patient data using an instruction-tuned language model.

**Key features:**
- Uses LLMs for controlled text generation
- Post-generation validation for privacy
- Explainable evaluation metrics
- Designed for healthcare compliance

📂 Folder: `clinSynthAI/`

---

### 2️⃣ RadExplainAI — Radiology Report Generation

RadExplainAI converts raw radiology findings into structured
radiology reports.

**Design principle:**
- LLM used only for language rewriting
- Safety-critical impressions generated using rule-based logic
- Validation and evaluation pipelines included

📂 Folder: `radExplainAI/`

---

## 🛠️ Tech Stack

- Python
- Hugging Face Transformers
- Google FLAN-T5
- Rule-based validation
- macOS-compatible execution

---

## 🚀 How to Run

### 1. Create virtual environment
```bash
python3 -m venv genai-env
source genai-env/bin/activate
pip install transformers torch pandas


### 2.Run ClinSynthAI
cd clinSynthAI
python test_gen.py

### 3.Run RadExplainAI
cd radExplainAI
python test_gen.py

