import ollama
import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from _types import ListResponse, ChatRequest, ChatResponse
from typing import Dict, Any
from _helpers import verify_github_token


router = APIRouter()

@router.get("/tags")
async def get_tags():
    """
    Get the list of tags available in Ollama.
    """
    try:
        models: ListResponse = ollama.list()
        return models.model_dump()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bob_AI(request: ChatRequest, user: Dict[str, Any] = Depends(verify_github_token)):
    try:
        print ("user", user)
        model = request.model or "llama2"
        result = ollama.chat(model=model, messages=request.messages, stream=True) # type: ignore

        def event_stream():
            for chunk in result:
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield json.dumps({"message": {"content": content}}) + "\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/plain"  # Treat as NDJSON
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
