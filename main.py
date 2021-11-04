# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastApi
from fastapi import FastAPI
from fastapi import status

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

class UserRegister(Users):
     password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )
   
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

# Path Parameter

## Users

@app.post(
    path="/auth/signup",
    response_model=Users,
    status_code= status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup():
    """
    Sign up 

    This path operation register a user in the app.

    Parameters:
        - Request body parameter
            - user: UserRegister 
    
    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str 
        - birth_date: str

    """
    pass 

@app.post(
    path="/auth/loginup",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def loginup():
    pass 

@app.get(
    path="/users",
    response_model=List[Users],
    status_code= status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"]
)
def show_all_user():
    pass 

@app.get(
    path="/users/{user_id}",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Get a specific User",
    tags=["Users"]
)
def show_a_user():
    pass 

@app.put(
    path="/users/{user_id}/update",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Updates a specific User",
    tags=["Users"]
)
def update_user():
    pass 

@app.delete(
    path="/users/{user_id}/delete",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_user():
    pass 

## Tweets

@app.get(
    path="/",
    response_model=list[Tweet],
    status_code= status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter Api":"Working!"}

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Show a specific Tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass 

@app.post(
    path="/tweets",
    response_model=Tweet,
    status_code= status.HTTP_201_CREATED,
    summary="Create a new Tweet",
    tags=["Tweets"]
)
def create_a_tweet():
    pass 

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Updates a specific Tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Delete a specific Tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass 