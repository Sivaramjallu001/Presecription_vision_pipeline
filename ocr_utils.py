import json
import re
import ast
import os
import pytesseract
from PIL import Image
import google.generativeai as genai
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

genai.configure(api_key="YOUR-API-KEY")  # Replace with your actual key


def extract_text(image_path):
    """
    Main function to extract text and structured data from a prescription image.
    Tries Gemini first; falls back to Tesseract OCR if Gemini fails.
    """
    try:
        return extract_with_gemini(image_path)
    except Exception as e:
        print("⚠️ Gemini failed. Falling back to Tesseract. Error:", e)
        return extract_with_tesseract(image_path)


def extract_with_gemini(image_path):
    model = genai.GenerativeModel("gemini-1.5-flash")
    ext = os.path.splitext(image_path)[1].lower()

    if ext == ".pdf":
        # Convert PDF to image
        images = convert_from_path(image_path, dpi=300)
        image = images[0]  # Use first page only
    else:
        # Open image directly
        image = Image.open(image_path)
    

    prompt = (
        "Extract the following fields from this medical prescription image:\n"
        "- Patient Name\n- Patient Age\n- Patient Gender\n"
        "- Doctor Name\n- Doctor Registration Number\n"
        "- Date of prescription\n"
        "- Medications (Name, Dosage, Frequency, Duration)\n"
        "- Instructions or additional notes\n"
        "Return ONLY a raw JSON object using double quotes, without markdown, no triple backticks."
    )

    response = model.generate_content([prompt, image])
    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = re.sub(r"```(?:json)?\n?", "", response_text)
        response_text = response_text.rstrip("`").strip()

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        data = ast.literal_eval(response_text)

    return "", normalize_data(data)


def extract_with_tesseract(image_path: str):
    try:
        # Check if PDF and convert to image
        if image_path.lower().endswith(".pdf"):
            images = convert_from_path(image_path, dpi=300)
            if not images:
                raise ValueError("No pages found in PDF.")
            image = images[0]  # First page only
        else:
            image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        # Add a simple parser fallback
        parsed_data = {
            "Doctor": {
                "Name": "N/A",
                "RegistrationNumber": "N/A"
            },
            "Patient": {
                "Name": "N/A",
                "Age": "N/A",
                "Gender": "N/A"
            },
            "Date": "N/A",
            "Medicines": [],
            "Notes": "N/A"
        }

        return text, parsed_data

    except Exception as e:
        raise RuntimeError(f"Tesseract fallback failed: {e}")



def find_line(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else "N/A"


def normalize_data(data):
    """
    Normalize extracted data into a consistent structure.
    Fills missing fields with 'N/A' or appropriate default.
    """
    return {
        "Patient": {
            "Name": data.get("Patient Name", "N/A"),
            "Age": data.get("Patient Age", "N/A"),
            "Gender": data.get("Patient Gender", "N/A")
        },
        "Doctor": {
            "Name": data.get("Doctor Name", "N/A"),
            "RegistrationNumber": data.get("Doctor Registration Number", "N/A")
        },
        "Date": data.get("Date of prescription", "N/A"),
        "Medicines": data.get("Medications", []),
        "Notes": data.get("Instructions or additional notes", "N/A"),
        "raw_text": data.get("raw_text", "")
    }
