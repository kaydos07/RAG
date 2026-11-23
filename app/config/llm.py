from google import genai
from google.genai import types


from .settings import settings

client = genai.Client(api_key=settings.MODEL_API_KEY)   

model_name = settings.EMBEDDING_MODEL_NAME



def embedding(content: str, task_type: str): 
    res = client.models.embed_content(
        model=model_name,
        contents=content,
        config=types.EmbedContentConfig(
            output_dimensionality=1536,
            task_type=task_type                              #RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY
        )
    )
    
    return res.embeddings[0].values
