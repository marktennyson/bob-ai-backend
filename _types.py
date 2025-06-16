from pydantic import BaseModel
from typing import List
from ollama._types import * # type: ignore

class SaveUserResponse(BaseModel):
    message: str

class AIModel(BaseModel):
    id: str
    name: str
    digest: str

class AIModelListResponse(BaseModel):
    models: List[AIModel]

class User(BaseModel):
    email: str
    name: str
    provider: str
    