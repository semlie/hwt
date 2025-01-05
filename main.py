from core.utils import get_files_with_extensions, list_to_jsonl, load_image, load_pdf, pdf_to_image
from core.agents import ChatGoogleGenerativeAIAgent
from dotenv import load_dotenv
from core.models import RestaurantMenuExtractionResult
load_dotenv()


def process_html(html_path):
    with open(html_path, "r") as f:
        html = f.read()

    agent = ChatGoogleGenerativeAIAgent()
    llm_res = agent.generate_response_with_html(html)
    res = RestaurantMenuExtractionResult(
        file_name=html_path, **llm_res.model_dump())
    return res.model_dump()


def process_image(image_path):
    agent = ChatGoogleGenerativeAIAgent()
    image = load_image(image_path)
    llm_res = agent.generate_response_with_image(image)
    res = RestaurantMenuExtractionResult(
        file_name=image_path, **llm_res.model_dump())
    return res.model_dump()


def process_pdf(pdf_path):
    pdf_text = pdf_to_image(pdf_path)
    # txt = "\n ".join([page.page_content for page in pdf_text])
    agent = ChatGoogleGenerativeAIAgent()
    llm_res = agent.generate_response_with_pdf(pdf_text)
    res = RestaurantMenuExtractionResult(
        file_name=pdf_path, **llm_res.model_dump())
    return res.model_dump()


# read all files in a folder
def run(folder_path):
    result = []
    valid_extensions = ["pdf", "jpg", "html", "png"]

    files_by_ext = get_files_with_extensions(folder_path, valid_extensions)
    for ext, files in files_by_ext.items():
        for file in files:
            try:
                if ext == "pdf":
                    pages = process_pdf(file)
                    print(f"Loaded pdf from {
                          file}, the llm results are: {pages}")
                    result.append(pages)
                elif ext in ["jpg", "png"]:
                    img = process_image(file)
                    print(f"Loaded image from {
                          file} the llm results are: {img}")
                    result.append(img)
                elif ext == "html":
                    html = process_html(file)
                    print(f"Loaded html from {
                          file}, the llm results are: {html}")
                    result.append(html)
                else:
                    print(f"Unsupported file type: {ext}")
            except Exception as e:
                print(f"Error processing file {file}: {e}")
    return result


if __name__ == "__main__":
    res = run("./data")
    list_to_jsonl(res, "output.jsonl")
    print(res)
