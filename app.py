import streamlit as st
import json
import os
import pandas as pd
from utils.ocr_utils import extract_text
from utils.file_utils import save_uploaded_file

# Page setup
st.set_page_config(page_title="Prescription Vision Pipeline", layout="wide")
st.title("🩺 Prescription Vision Pipeline")
st.write("Upload a prescription image to extract structured data.")

# Upload block
uploaded_file = st.file_uploader("Upload Prescription Image", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    image_path = save_uploaded_file(uploaded_file)

    with st.spinner("🔍 Extracting prescription data..."):
        raw_text, parsed_data = extract_text(image_path)

    st.success("✅ Extraction complete!")

    # Show raw image
    st.image(image_path, caption="Uploaded Prescription", use_container_width=False, width=200)

    # Editable preview form
    if parsed_data:
        st.success("✅ Data extracted. You can review or edit the fields below.")

        with st.form("edit_form"):
            st.subheader("📝 Prescription Preview (Editable)")

            # Patient Info
            patient = parsed_data.get("Patient", {})
            patient_name = st.text_input("Patient Name", value=patient.get("Name", "N/A"))
            patient_age = st.text_input("Patient Age", value=patient.get("Age", "N/A"))
            patient_gender = st.text_input("Patient Gender", value=patient.get("Gender", "N/A"))

            # Doctor Info
            doctor = parsed_data.get("Doctor", {})
            doctor_name = st.text_input("Doctor Name", value=doctor.get("Name", "N/A"))
            doctor_reg = st.text_input("Doctor Registration Number", value=doctor.get("RegistrationNumber", "N/A"))

            # Other Fields
            date = st.text_input("Date of Prescription", value=parsed_data.get("Date", "N/A"))
            notes = st.text_area("Additional Notes", value=parsed_data.get("Notes", "N/A"))

            # Medicines
            medicines = parsed_data.get("Medicines", [])
            st.markdown("### 💊 Medicines")
            for i, med in enumerate(medicines):
                st.text_input(f"Medicine {i+1} - Name", value=med.get("Name", ""))
                st.text_input(f"Medicine {i+1} - Dosage", value=med.get("Dosage", ""))
                st.text_input(f"Medicine {i+1} - Frequency", value=med.get("Frequency", ""))
                st.text_input(f"Medicine {i+1} - Duration", value=med.get("Duration", ""))

            submitted = st.form_submit_button("💾 Save Changes")
            if submitted:
                st.success("✅ Your changes have been saved (in memory).")

    # JSON preview
    st.subheader("📋 Extracted Details (Raw JSON)")
    st.json(parsed_data)

    # Raw OCR fallback text
    if raw_text.strip():
        with st.expander("🔁 Raw OCR Text (Tesseract Fallback)"):
            st.code(raw_text)

    # JSON download
    st.download_button("📥 Download JSON", json.dumps(parsed_data, indent=4),
                       file_name="prescription.json", mime="application/json")

    # CSV download for medicines
    if parsed_data.get("Medicines"):
        df = pd.DataFrame(parsed_data["Medicines"])
        st.download_button("📥 Download Medicines CSV", df.to_csv(index=False),
                           file_name="medicines.csv", mime="text/csv")
