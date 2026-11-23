from fastapi import FastAPI
from pydantic import BaseModel
from .services.agent import invoke_AI

client = FastAPI()

class AIRequest(BaseModel):
    content: str


@client.post("/AI")
def answer(req: AIRequest): 
     return invoke_AI(req.content)