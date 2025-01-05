import json
from typing import List, Dict, Any
import os
from langchain.document_loaders import PyPDFLoader
import base64
from PIL import Image
from pdf2image import convert_from_path


import io


def load_pdf(pdf_path):
    """Loads a PDF file using PyPDFLoader and returns a list of Document objects."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return pages


def pdf_to_image(pdf_path):
    """Converts a PDF file to a list of base64 encoded images."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    images = convert_from_path(pdf_path)

    image_data = []
    for x in range(len(pages)):
        img = images[x]
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        image_data.append(
            {"page_content": pages[x].page_content, "image": img_str})
    return image_data


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


def list_to_jsonl(data: List[Dict[Any, Any]], output_file: str) -> None:
    """
    Convert a list of dictionaries to a JSONL file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                # Convert each dictionary to a JSON string and write it with a newline
                json_line = json.dumps(item, ensure_ascii=False)
                f.write(json_line + '\n')

    except Exception as e:
        raise Exception(f"Error writing JSONL file: {str(e)}")
