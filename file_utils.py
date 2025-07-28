import os
from werkzeug.utils import secure_filename
from PIL import Image
from pdf2image import convert_from_path

def save_uploaded_file(file, data_folder='data/raw/', upload_folder='static/uploads/'):
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_ext = filename.split('.')[-1].lower()
    raw_path = os.path.join(data_folder, filename)

    # Save original file
    file.save(raw_path)

    # Convert to image if PDF
    if file_ext == 'pdf':
        images = convert_from_path(raw_path)
        image_path = os.path.join(upload_folder, f"{filename}.jpg")
        images[0].save(image_path)
    else:
        image = Image.open(raw_path)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

    return image_path
