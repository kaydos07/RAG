import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_protocol import Checkpoint
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.schema import tools, system_instruction

load_dotenv()



client = genai.Client(api_key=os.getenv("MODEL_API_KEY"))   

def split_content(content: str, chunk_size: int):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size/10
    )
    split_content = text_splitter.split_text(content)
    
    return split_content

def embedding(content: str, task_type: str): 
    res = client.models.embed_content(
        model=os.getenv('EMBEDDING_MODEL_NAME'),
        contents=content,
        config=types.EmbedContentConfig(
            output_dimensionality=1536,
            task_type=task_type                              #RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY
        )
    )
    
    return res.embeddings[0].values

response = client.interactions.create(
    model=os.getenv('MODEL_NAME'),
    input="what is milk",
    tools=tools,
    system_instruction=system_instruction
)