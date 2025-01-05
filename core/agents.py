
from langchain_google_genai import ChatGoogleGenerativeAI
from core.prompts import prompt_template_html, prompt_template_img, prompt_template_pdf, prompt_template_txt
from core.models import RestaurantMenu

# "gemini-1.5-flash"  # "gemini-2.0-flash-exp","gemini-1.5-flash"
model_v = "gemini-1.5-flash"


class ChatGoogleGenerativeAIAgent:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model=model_v)

    def generate_response_with_image(self, image_data):
        prompt = prompt_template_img(image_data)
        agent = prompt | self.model.with_structured_output(RestaurantMenu)
        return agent.invoke({"source_input_type": "image"})

    def generate_response_with_pdf(self, text):
        prompt = prompt_template_pdf(text)
        agent = prompt | self.model.with_structured_output(RestaurantMenu)
        return agent.invoke({"source_input_type": "pdf"})

    def generate_response_with_html(self, html):
        prompt = prompt_template_html()
        agent = prompt | self.model.with_structured_output(RestaurantMenu)
        return agent.invoke({"source_input_type": "html", "the_html": html})
