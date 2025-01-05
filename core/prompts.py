from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage


system_prompt_txt = "you are a pro export in the resterunt industry and you are tasked to analyes menu for a resterunt. you are given a menu in the form of a image and you are asked to extract the menu items from the image. or text. You can use your knowledge to extract the menu items from the image or text and fill the category, or ingredients of the menu items."
instract_prompt_text = "EXTRACT MENUE FROM {source_input_type}"


def prompt_template_img(image_data):
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt_txt),
        HumanMessage(
            content=[
                {"type": "text", "text": instract_prompt_text},

                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                },
            ],
        )
    ])


def prompt_template_txt():
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt_txt),
        ("user", "This is the text from pdf: {the_text}"),
        ("user", instract_prompt_text)


    ])


def prompt_template_html():
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt_txt),
        ("user", "This is the html content: html```{the_html}```"),
        ("user", instract_prompt_text)
    ])
