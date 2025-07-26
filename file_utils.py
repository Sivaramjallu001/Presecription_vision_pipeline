import os
import uuid

def save_uploaded_file(uploaded_file, save_dir="uploaded_prescriptions"):
    """
    Saves the uploaded file to the specified directory with a unique name.

    Args:
        uploaded_file (UploadedFile): File object from Streamlit uploader.
        save_dir (str): Directory where the image will be saved.

    Returns:
        str: Full path of the saved file.
    """
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Generate a unique filename using UUID
    file_ext = uploaded_file.name.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"

    file_path = os.path.join(save_dir, unique_filename)

    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
