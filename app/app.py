from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from contextlib import asynccontextmanager
from database import create_db_and_tables


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

