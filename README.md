# 🩺 Prescription Vision Pipeline

A Streamlit-based AI application that extracts **structured medical data** from **prescription images or PDFs** using **Gemini Vision OCR** with a **Tesseract fallback**. This tool helps digitize and clean prescription records for healthcare workflows.

---

## 🚀 Features

- 📤 Upload prescriptions in **JPG, PNG, or PDF**
- 🧠 Extracts text using **Gemini Vision API**
- 🔁 Fallback to **Tesseract OCR** if Gemini fails
- 📝 Parses key fields:
  - Doctor Name
  - Patient Info
  - Medicines
  - Instructions
  - Date
- ✍️ Editable structured data preview
- 💾 Download as **JSON** or **CSV**
- ⚡ Optimized for performance with image compression
- 🔒 No external database or login needed

---

## 📁 Project Structure

prescription_vision_pipeline/
│
├── app.py # Streamlit UI logic
├── ocr_utils.py # Gemini + Tesseract OCR + parsing
├── file_utils.py # File saving & compression
├── requirements.txt # Python dependencies
└── extracted/ # Folder for uploaded images


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
