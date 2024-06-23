import os
import fitz  # PyMuPDF

def ensure_upload_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_file(file, folder):
    file_path = os.path.join(folder, file.filename)
    file.save(file_path)
    return file_path

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text
