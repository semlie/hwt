from core.utils import get_files_with_extensions, load_image, load_pdf
from core.agents import ChatGoogleGenerativeAIAgent
from dotenv import load_dotenv
from core.models import RestaurantMenuExtractionResult
load_dotenv()


def process_html(html_path):
    with open(html_path, "r") as f:
        html = f.read()
    return html


def process_image(image_path):
    agent = ChatGoogleGenerativeAIAgent()
    image = load_image(image_path)
    llm_res = agent.generate_response_with_image(image)
    res = RestaurantMenuExtractionResult(
        file_name=image_path, **llm_res.model_dump())
    return res.model_dump()


def process_pdf(pdf_path):
    pdf_text = load_pdf(pdf_path)
    txt = "\n ".join([page.page_content for page in pdf_text])
    agent = ChatGoogleGenerativeAIAgent()
    llm_res = agent.generate_response_with_pdf(txt)
    res = RestaurantMenuExtractionResult(
        file_name=pdf_path, **llm_res.model_dump())
    return res.model_dump()


# read all files in a folder
def run(folder_path):
    valid_extensions = ["pdf"]  # ["pdf", "jpg", "html", "png"]

    files_by_ext = get_files_with_extensions(folder_path, valid_extensions)
    for ext, files in files_by_ext.items():
        for file in files:
            if ext == "pdf":
                pages = process_pdf(file)
                print(f"Loaded pdf from {file}, the llm results are: {pages}")
            elif ext in ["jpg", "png"]:
                res = process_image(file)
                print(f"Loaded image from {file} the llm results are: {res}")
            elif ext == "html":
                html = process_html(file)
                print(f"Loaded html from {file}")
            else:
                print(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    run("./data")
