# Python
import json
import os
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
from fastapi.exceptions import HTTPException

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path
from starlette.responses import Response

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

class BaseTweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )

class Tweet(BaseTweet):
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
def show_a_user(user_id: str = Path(
        ...,
        title="User Id",
        description="Id of the user"
    )):
    """
    Show a user
    
    This path operation show all users in the app
    
    Parameters: user_id 
    
    Returns json list with an user in the app, with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str 
        - birth_date: date        
      """
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as f:
            results = json.load(f)

        for user in results:
            if user['user_id'] == user_id:
                return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

@app.put(
    path="/users/{user_id}/update",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Updates a specific User",
    tags=["Users"]
)
def update_user(user_id: str = Path(
        ...,
        title='User Id',
        description='ID of the user to update'),
        user: UserRegister = Body(...)):
        """
        Update a user
            
        This path operation update an user in the app
            
        Parameters: user_id: str
                    user: UserRegister
            
        Returns json list with an user update in the app, with the following keys:
            - user_id: UUID
            - email: Emailstr
            - first_name: str
            - last_name: str 
            - birth_date: date        
        """
        index = None 
        if os.path.exists("users.json"):
            with open("users.json", "r+", encoding='utf-8') as f:
                users = json.load(f)

                for idx, raw_user in enumerate(users):
                    if raw_user['user_id'] == user_id:
                        index = idx
                        break 

                if index is not None:
                    users[index].update({
                        **user.dict(),
                        'user_id' : str(user.user_id),
                        'birth_date' : str(user.birth_date),
                        'updated_at': str(datetime.now()), 
                    })

                    f.seek(0)
                    f.truncate()
                    f.write(json.dumps(users)) 

        if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.')  

        return users[index]     

@app.delete(
    path="/users/{user_id}/delete",
    response_model=Users,
    status_code= status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_user(user_id : str = Path(...,
                title='Id User',
                description='Id of the user a delete'
    )):
    """
    Delete a User
    
    Parameters:
    - user_id: str 
    
    returns HTTP_204_NO_CONTENT 
    """
    found = False
    if os.path.exists("users.json"):
        with open("users.json", 'r+', encoding='utf-8') as f:
            raw_users = json.load(f)

            users=[]

            for raw_user in raw_users:
                if raw_user["user_id"] == user_id:
                    found = True 
                else:
                    users.append(raw_user)
            if found:
                f.seek(0)
                f.truncate()
                f.write(json.dumps(users))

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT,)       


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
def show_a_tweet(tweet_id: str = Path(
        ...,
        title="Tweet Id",
        description="Tweet Id of an user"
    )):
    """
    Show a Tweet 
    
    This path operation show a tweet in the app
    
    Parameters: tweet_id 
    
    Returns json list with a tweet in the app, with the following keys:
        tweet_id: UUID 
        content: str
        created_at: datetime
        updated_at: Optional[datetime]
        by: User     
      """
    if os.path.exists("tweet.json"):
        with open("tweet.json", "r", encoding="utf-8") as f:
            results = json.load(f)

        for tweet in results:
            if tweet['tweet_id'] == tweet_id:
                return tweet
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")

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
def update_a_tweet(tweet_id: str = Path(
        ...,
        title='Tweet Id',
        description='ID of the tweet to update'),
        tweet: BaseTweet = Body(...),)-> Tweet:
        """
        Update a tweet
            
        This path operation update a tweet in the app
            
        Parameters: tweet_id: str
                    tweet: Tweet
            
        returns a json with a basic tweet information:
            tweet_id: UUID
            content_ str
            created_at: datetime
            updated_at: Optional[datetime]
            by: user    
        """
        index = None 
        if os.path.exists("tweet.json"):
            with open("tweet.json", "r+", encoding='utf-8') as f:
                tweets = json.load(f)

                for idx, raw_tweet in enumerate(tweets):
                    if raw_tweet['tweet_id'] == tweet_id:
                        index = idx
                        break 

                if index is not None:
                    tweets[index].update({
                        **tweet.dict(),
                        'tweet_id' : str(tweet.tweet_id),
                        'updated_at': str(datetime.now()), 
                    })

                    f.seek(0)
                    f.truncate()
                    f.write(json.dumps(tweets)) 

        if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='Tweet not found.')  

        return tweets[index]     

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code= status.HTTP_200_OK,
    summary="Delete a specific Tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id : str = Path(...,
                title='Id Tweet',
                description='Id of the tweet a delete'
    )):
    """
    Delete a Tweet
    
    Parameters:
    - tweet_id: str 
    
    returns HTTP_204_NO_CONTENT 
    """
    found = False
    if os.path.exists("tweet.json"):
        with open("tweet.json", 'r+', encoding='utf-8') as f:
            raw_tweets = json.load(f)

            tweets=[]

            for tweet in raw_tweets:
                if tweet["tweet_id"] == tweet_id:
                    found = True 
                else:
                    tweets.append(tweet)
            if found:
                f.seek(0)
                f.truncate()
                f.write(json.dumps(tweets))

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)       

