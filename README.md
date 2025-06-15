# Ollama Chat API

A FastAPI backend for chatting with Ollama models.

## Features
- Chat endpoint for interacting with Ollama models (default: mistral)
- List available Ollama models/tags
- Typed request/response models using Pydantic

## Requirements
- Python 3.12+
- [Ollama Python package](https://pypi.org/project/ollama/)
- FastAPI
- Pydantic

## Setup
1. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install fastapi ollama pydantic uvicorn
   ```

## Running the API
Start the FastAPI server with Uvicorn:
```bash
uvicorn app:app --reload
```

## API Endpoints

### `GET /`
Returns a welcome message.

### `GET /tags`
Returns a list of available Ollama models/tags.

**Response Example:**
```json
{
  "models": [ ... ]
}
```

### `POST /chat`
Chat with an Ollama model.

**Request Body:**
```json
{
  "messages": [
    { "role": "user", "content": "Hello!" },
    { "role": "assistant", "content": "Hi! How can I help you?" }
  ],
  "model": "mistral" // optional, defaults to "mistral"
}
```

**Response:**
```json
{
  "response": "...model reply..."
}
```

## Example Usage (Python)
```python
import requests

resp = requests.post("http://localhost:8000/chat", json={
    "messages": [{"role": "user", "content": "Hello!"}]
})
print(resp.json())
```

## License
MIT
