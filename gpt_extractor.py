from dotenv import load_dotenv
from prompt import build_field_prompt
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_field_information(field_name, field_description, page_number, page_text):
    # fieldname, field_description, page_number, page_text .
    prompt=build_field_prompt(field_name, field_description, page_number, page_text)
    
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an intelligent document extraction assistant."},
        {"role": "user", "content": prompt.strip()}
    ],
    temperature=0.2
    )

    return response.choices[0].message.content