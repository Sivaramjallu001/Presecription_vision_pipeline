# 🩺 Prescription Vision Pipeline

A Streamlit-based web application to extract structured information from handwritten or printed medical prescription images using Google Gemini and Tesseract OCR as fallback.

---

## 📌 Table of Contents

- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Appendix](#appendix)

---

## 📖 Introduction

Healthcare records are often documented in unstructured handwritten or printed formats. This project leverages modern OCR techniques and generative AI (Gemini) to extract meaningful structured data from prescription images, including patient details, doctor information, medications, and notes.

---

## ❗ Problem Statement

Manual extraction of prescription data is time-consuming and error-prone. There's a need for an automated tool that can:
- Digitize handwritten prescriptions
- Extract structured data from them
- Provide an editable preview
- Handle both images and PDFs
- Work even if the AI model fails (via OCR fallback)

---

## 🌟 Features

- ✅ Upload `.jpg`, `.jpeg`, `.png`, or `.pdf` prescriptions
- ✅ Extracts:
  - Patient Name, Age, Gender
  - Doctor Name, Registration Number
  - Prescription Date
  - Medicines (Name, Dosage, Frequency, Duration)
  - Additional Notes
- ✅ Uses Gemini API as primary model
- ✅ Fallback to Tesseract OCR if Gemini fails
- ✅ Editable preview form
- ✅ Download structured JSON and CSV

---

## 🏗 Architecture

```text
           ┌────────────┐
           │  Upload    │
           │  Image/PDF │
           └────┬───────┘
                ↓
      ┌────────────────────┐
      │ Gemini (AI Parsing)│
      └────────┬───────────┘
               ↓ fallback
     ┌───────────────────────┐
     │ Tesseract OCR (Backup)│
     └────────┬──────────────┘
              ↓
      ┌────────────────────┐
      │ Extract & Normalize│
      └────────┬───────────┘
               ↓
     ┌─────────────────────────────┐
     │ Streamlit Editable Preview  │
     └────────┬────────────────────┘
              ↓
     ┌────────────────────────────────────┐
     │ JSON/CSV Download of Prescription  │
     └────────────────────────────────────┘


## 📁 Project Structure
```bash
prescription_vision_pipeline/
│
├── app.py # Streamlit UI logic
├── ocr_utils.py # Gemini + Tesseract OCR + parsing
├── file_utils.py # File saving & compression
├── requirements.txt # Python dependencies
└── extracted/ # Folder for uploaded images
```

🛠️ Installation

1. Clone this repository:

```bash
git clone https://github.com/Sivaramjallu001/Presecription_vision_pipeline.git
cd prescription-vision-pipeline

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export GEMINI_API_KEY="your_key"     # Linux/Mac
set GEMINI_API_KEY="your_key"        # Windows

streamlit run app.py
