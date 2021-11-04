# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastApi
from fastapi import FastAPI

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Users(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    ) 
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    ) 
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    create_at: datetime =Field(default=datetime.now())
    update_at: Optional[datetime] =Field(default=None) 
    by: Users = Field(...)




@app.get(path="/")
def home():
    return {"Twitter Api":"Working!"}