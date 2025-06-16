import ollama
from fastapi import APIRouter, HTTPException, Depends
from _types import (
    ListResponse, 
    AIModelListResponse, 
    AIModel, User, 
    SaveUserResponse
)
from app.routes import chat
from _helpers import verify_jwt_token
from database import SessionDep
from app.sqlmodels import UserSQLModel


router = APIRouter()
router.include_router(chat.router, prefix="/chat", tags=["chat"])

@router.get("/models", response_model=AIModelListResponse)
@router.get("/tags", response_model=AIModelListResponse)
async def get_tags():
    """
    Get the list of tags available in Ollama.
    """
    try:
        models: ListResponse = ollama.list()
        return AIModelListResponse(models=[AIModel(
            id=model.model or "",
            name=((model.model or "").split(":")[0]).capitalize(),
            digest=model.digest or ""
        ) for model in models.models])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-user", response_model=SaveUserResponse)
def save_user(db: SessionDep, user: User = Depends(verify_jwt_token)):
    try:
        db_user = UserSQLModel(**user.model_dump())
        db.add_user(db_user)
        return {"message": "User data saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
