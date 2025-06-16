from dotenv import load_dotenv; load_dotenv()
import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session as SessionBase
from app.sqlmodels import UserSQLModel

# Database configuration
sqlite_file_name = "bob-ai.db"
engine_url = f"sqlite:///{sqlite_file_name}"

engine_url = os.environ.get("DATABASE_URL", engine_url)

connect_args = {"check_same_thread": True}
engine = create_engine(engine_url, connect_args=connect_args)

class Session(SessionBase):
    def add_user(self, user: UserSQLModel) -> UserSQLModel:
        self.add(user)
        self.commit()
        self.refresh(user)
        return user

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")