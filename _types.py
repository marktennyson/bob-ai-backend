from pydantic import BaseModel
from typing import Optional, List
from ollama._types import * # type: ignore

class ChatRequest(BaseModel):
    model: Optional[str]
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

class Model(BaseModel):
    name: str
    digest: str

class ModelListResponse(BaseModel):
    models: List[str]
    