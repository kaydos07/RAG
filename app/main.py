from fastapi import FastAPI
from app.schemas.chats_schema import ChatRequest
from .services.agent import invoke_AI
from .config.mcp_manager import mcp_manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await mcp_manager.connect()
        print(f"[MCP] Loaded tools: {mcp_manager.tool_names}")
        yield
    finally:
        await mcp_manager.disconnect()

client = FastAPI(lifespan=lifespan)


@client.post("/AI")
async def answer(req: ChatRequest): 
     return {"message" : await invoke_AI(req.content)}