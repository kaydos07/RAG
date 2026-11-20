from http import client
import os
from pydoc import cli
from urllib import response
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("MODEL_API_KEY"))

response = client.interactions.create(
    model=os.getenv('MODEL_NAME'),
    input="what is milk"
)

print(response.output_text)