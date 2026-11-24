from fastapi import FastAPI
from schemas.chats_schema import ChatRequest
from .services.agent import invoke_AI
from .config import mcp_manager
from contextlib import asynccontextmanager

@asynccontextmanager
def lifespan():
    mcp_manager.connect()
    yield
    mcp_manager.disconnect()

client = FastAPI(lifespan=lifespan)


@client.post("/AI")
def answer(req: ChatRequest): 
     return {"message" : invoke_AI(req.content)}