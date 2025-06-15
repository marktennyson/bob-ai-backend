import httpx
import time
from fastapi import HTTPException, Request
from typing import Dict, Any, Tuple

TOKEN_CACHE:Dict[str, Tuple[Dict[str, Any], float]] = {}

def is_token_cached_valid(token: str) -> bool:
    return token in TOKEN_CACHE and TOKEN_CACHE[token][1] > time.time()

async def get_cached_or_fetch_user(token: str) -> Dict[str, Any] | Any:
    if is_token_cached_valid(token):
        return TOKEN_CACHE[token][0]

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"}
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid GitHub token")

    user_data = resp.json()
    # Cache it for 5 minutes
    TOKEN_CACHE[token] = (user_data, time.time() + 300)
    return user_data

async def verify_github_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    return await get_cached_or_fetch_user(token)