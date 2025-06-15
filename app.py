from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import ollama, json
from ollama._types import ListResponse

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: Optional[str]
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

class Model(BaseModel):
    name: str
    digest: str

class ModelListResponse(BaseModel):
    models: List[str]
    

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

@app.get("/api/tags")
async def get_tags():
    """
    Get the list of tags available in Ollama.
    """
    try:
        models: ListResponse = ollama.list()
        return models.model_dump()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat_with_ollama(request: ChatRequest):
    try:
        ollama_messages = [
            {"role": m.role, "content": m.content} for m in request.messages
        ]
        model = request.model or "llama2"
        result = ollama.chat(model=model, messages=ollama_messages, stream=True)

        def event_stream():
            for chunk in result:
                content = chunk.get("message", {}).get("content", "")
                if content:
                    # Send as a line-delimited JSON object
                    yield json.dumps({"message": {"content": content}}) + "\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/plain"  # Treat as NDJSON
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
