from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr, UUID4


class UserSQLModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr | None = Field(default=None, index=True, unique=True)
    provider: str = Field(index=True)
    chat_history: list["ChatHistorySQLModel"] = Relationship(back_populates="user")


class ChatHistorySQLModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID4 = Field(index=True, unique=True)
    responses: str
    timestamp: str
    user_id: int | None = Field(default=None, foreign_key="usersqlmodel.id")
    user: UserSQLModel = Relationship(back_populates="chat_history")