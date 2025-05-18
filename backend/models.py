from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# https://www.better-auth.com/docs/concepts/database#session
# match the better-auth database schema

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    emailVerified: bool = Field(default=False)
    image: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # 设置与 UserSession 模型的关系
    sessions: "UserSession" = Relationship(back_populates="user")

class UserSession(SQLModel, table=True):
    __tablename__ = "session"

    id: str = Field(primary_key=True)
    userId: str = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    expiresAt: datetime
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # 设置与 User 模型的关系
    user: "User" = Relationship(back_populates="sessions")

