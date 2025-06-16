from fastapi import HTTPException, Request
from jose import jwt, exceptions as jwt_exceptions
import os, json
from _types import User
from ollama._types import ChatResponse
from typing import Iterator, Any, AsyncGenerator

async def verify_jwt_token(request: Request) -> User:
    """
    Verify the JWT token from the request headers.
    """
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
        return User(email=payload.get("email", ""), name=payload.get("name", ""), provider=payload.get("provider", ""))
    
    except jwt_exceptions.JWTError:
        raise HTTPException(status_code=403, detail="Forbidden")

async def event_stream(chat_response: Iterator[ChatResponse]) -> AsyncGenerator[str, Any]:
    for chunk in chat_response:
        content = chunk.get("message", {}).get("content", "")
        if content:
            yield json.dumps({"message": {"content": content}}) + "\n"