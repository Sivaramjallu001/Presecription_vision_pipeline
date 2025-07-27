import streamlit as st
import json
import pandas as pd
import uuid
import os
from utils.ocr_utils import extract_text
from utils.file_utils import save_uploaded_file
from pdf2image import convert_from_path

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
    ext = os.path.splitext(image_path)[1].lower()

    if ext == ".pdf":
        # Convert first page of PDF to image for display
        pdf_images = convert_from_path(image_path, dpi=200)
        st.image(pdf_images[0], caption="📄 PDF First Page", width=250)
    else:
        # Directly display image
        st.image(image_path, caption="🖼️ Uploaded Prescription", width=250)

    edited_data = {}
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
            updated_medicines = []
            for i, med in enumerate(medicines):
                name = st.text_input(f"Medicine {i+1} - Name", value=med.get("Name", ""))
                dosage = st.text_input(f"Medicine {i+1} - Dosage", value=med.get("Dosage", ""))
                frequency = st.text_input(f"Medicine {i+1} - Frequency", value=med.get("Frequency", ""))
                duration = st.text_input(f"Medicine {i+1} - Duration", value=med.get("Duration", ""))
                updated_medicines.append({
                    "Name": name,
                    "Dosage": dosage,
                    "Frequency": frequency,
                    "Duration": duration
                })

            submitted = st.form_submit_button("💾 Save Changes")
            if submitted:
                parsed_data = {
                    "Patient": {
                        "Name": patient_name,
                        "Age": patient_age,
                        "Gender": patient_gender
                    },
                    "Doctor": {
                        "Name": doctor_name,
                        "RegistrationNumber": doctor_reg
                    },
                    "Date": date,
                    "Notes": notes,
                    "Medicines": updated_medicines
                }

                # Save updated JSON
                output_id = str(uuid.uuid4())
                os.makedirs("saved_outputs", exist_ok=True)
                json_path = f"saved_outputs/prescription_{output_id}.json"
                with open(json_path, "w") as f:
                    json.dump(parsed_data, f, indent=4)

                # Save medicines CSV with additional fields
                rows = []
                for med in updated_medicines:
                    rows.append({
                        "Doctor": doctor_name,
                        "RegNo": doctor_reg,
                        "Patient": patient_name,
                        "Age": patient_age,
                        "Gender": patient_gender,
                        "Date": date,
                        "Medicine": med.get("Name", ""),
                        "Dosage": med.get("Dosage", ""),
                        "Frequency": med.get("Frequency", ""),
                        "Duration": med.get("Duration", ""),
                        "Notes": notes
                    })
                df = pd.DataFrame(rows)
                df.to_csv(f"saved_outputs/medicines_{output_id}.csv", index=False)

                st.success("✅ Your changes have been saved.")

    # JSON preview
    st.subheader("📋 Extracted Details (Raw JSON)")
    st.json(parsed_data)

    # Raw OCR fallback text
    if raw_text.strip():
        with st.expander("🔁 Raw OCR Text (Tesseract Fallback)"):
            st.code(raw_text)

    # Download buttons
    st.download_button("📥 Download Updated JSON", json.dumps(parsed_data, indent=4),
                       file_name="prescription.json", mime="application/json")

    if parsed_data.get("Medicines"):
        flat_rows = []
        for med in parsed_data["Medicines"]:
            flat_rows.append({
                "Doctor": parsed_data["Doctor"].get("Name", ""),
                "RegNo": parsed_data["Doctor"].get("RegistrationNumber", ""),
                "Patient": parsed_data["Patient"].get("Name", ""),
                "Age": parsed_data["Patient"].get("Age", ""),
                "Gender": parsed_data["Patient"].get("Gender", ""),
                "Date": parsed_data.get("Date", ""),
                "Medicine": med.get("Name", ""),
                "Dosage": med.get("Dosage", ""),
                "Frequency": med.get("Frequency", ""),
                "Duration": med.get("Duration", ""),
                "Notes": parsed_data.get("Notes", "")
            })
        flat_df = pd.DataFrame(flat_rows)
        st.download_button("📥 Download Medicines CSV", flat_df.to_csv(index=False),
                           file_name="medicines.csv", mime="text/csv")
