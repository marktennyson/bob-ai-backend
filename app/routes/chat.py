import ollama
from fastapi import  HTTPException, Depends, APIRouter
from fastapi.responses import StreamingResponse
from _types import ChatRequest, ChatResponse, User
from typing import Dict, Any, Optional
from pydantic import UUID4
from _helpers import verify_jwt_token, event_stream
# from app.sqlmodels import ChatHistorySQLModel

router: APIRouter = APIRouter()

@router.post("/{chat_uuid}", response_model=ChatResponse)
async def chat_with_bob_ai(
    chat_uuid:Optional[UUID4], 
    request: ChatRequest, 
    user: User = Depends(verify_jwt_token)
    ):
    try:
        # if chat_uuid:
            # chatHistory = ChatHistorySQLModel.
        return StreamingResponse(event_stream(ollama.chat(**request.model_dump())), media_type="text/event-stream") #type: ignore

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_chat_history_with_bob_ai(user: Dict[str, Any] = Depends(verify_jwt_token)):
    """
    Placeholder for chat history retrieval.
    This function should be implemented to return the chat history for the user.
    """
    # Implement your logic to retrieve chat history here
    return {"message": "Chat history is not implemented yet."}