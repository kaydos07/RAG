from pydantic import BaseModel

class AIRequest(BaseModel):
    content: str
