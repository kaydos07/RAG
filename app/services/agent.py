from ..config.settings import settings
from ..config.llm import client
from app.schemas.tools import tools
from app.prompts.system import system_instruction


model_name = settings.MODEL_NAME

def invoke_AI(content: str):
    response = client.interactions.create(
        model=model_name,
        input=content,
        tools=tools,
        system_instruction=system_instruction
    )