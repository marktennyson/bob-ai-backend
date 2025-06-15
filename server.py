import uvicorn as uv
from app import app

if __name__ == "__main__":
    uv.run(app, host="0.0.0.0", port=8000)
