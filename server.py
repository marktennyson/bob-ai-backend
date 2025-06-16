import uvicorn as uv
from dotenv import load_dotenv; load_dotenv()

if __name__ == "__main__":
    uv.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
