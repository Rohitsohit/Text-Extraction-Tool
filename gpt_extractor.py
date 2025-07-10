from dotenv import load_dotenv
from prompt import build_final_document_prompt
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_field_information(page_text):
    prompt=build_final_document_prompt(page_text)
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an intelligent document extraction assistant."},
        {"role": "user", "content": prompt.strip()}
    ],
    temperature=0.2
    )
    
    return response.choices[0].message.content