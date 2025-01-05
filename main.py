from core.utils import get_files_with_extensions, load_image, load_pdf
from core.agents import ChatGoogleGenerativeAIAgent
from dotenv import load_dotenv

load_dotenv()


def process_html(html_path):
    with open(html_path, "r") as f:
        html = f.read()
    return html


def process_image(image_path):
    image = load_image(image_path)

    return image


def process_pdf(pdf_path):
    return load_pdf(pdf_path)


# read all files in a folder
def run(folder_path):
    valid_extensions = ["png"]  # ["pdf", "jpg", "html", "png"]
    agent = ChatGoogleGenerativeAIAgent()
    files_by_ext = get_files_with_extensions(folder_path, valid_extensions)
    for ext, files in files_by_ext.items():
        for file in files:
            if ext == "pdf":
                pages = process_pdf(file)
                print(f"Loaded {len(pages)} pages from {file}")
            elif ext in ["jpg", "png"]:
                image = process_image(file)
                res = agent.generate_response_with_image(image)
                print(f"Loaded image from {file} the llm results are: {res}")
            elif ext == "html":
                html = process_html(file)
                print(f"Loaded html from {file}")
            else:
                print(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    run("./data")
