
from langchain_google_genai import ChatGoogleGenerativeAI
from core.prompts import prompt_template_img


class ChatGoogleGenerativeAIAgent:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    def generate_response_with_image(self, image_data):
        prompt = prompt_template_img(image_data)
        agent = prompt | self.model
        return agent.invoke({"source_input_type": "image"})
