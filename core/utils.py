import os
from langchain.document_loaders import PyPDFLoader
import base64
from PIL import Image

import io


def load_pdf(pdf_path):
    """Loads a PDF file using PyPDFLoader and returns a list of Document objects."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages


def load_image(image_path):
    """Loads image from path"""
    try:
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    except Exception as e:
        print(f"Error loading image at {image_path}: {e}")
        return None


def get_files_with_extensions(folder_path, valid_extensions):
    files_by_ext = {}
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            if file.lower().endswith(tuple(valid_extensions)):
                ext = file.split(".")[-1]
                files_by_ext.setdefault(ext, []).append(
                    f"{folder_path}/{file}")

    return files_by_ext
