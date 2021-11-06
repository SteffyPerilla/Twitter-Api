# Python
import json 
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
from fastapi import Body

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
    created_at: datetime =Field(default=datetime.now())
    updated_at: Optional[datetime] =Field(default=None) 
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
def signup(user: UserRegister = Body(...)):
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
        - birth_date: date 

    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user 

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
    """
    Show all user
    
    This path operation show all users in the app
    
    Parameters: N/A
    
    Returns json list with all users in the app, with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str 
        - birth_date: date        
      """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

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
    """
    Show all Tweets
    
    Parameters: NA
    
    returns a json list with all tweets in the app, with the following keys:
        tweet_id: UUID 
        content: str
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    with open("tweet.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        return results 

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
def create_a_tweet(tweet: Tweet = Body(...)):
    """
    Create a new Tweet 
    
    This path operation create a new tweet in the app 
    
    Parameters:
        - tweet: Tweet
        
    returns a json with a basic tweet information:
        tweet_id: UUID
        content_ str
        created_at: datetime
        updated_at: Optional[datetime]
        by: user
    """
    with open("tweet.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet 

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