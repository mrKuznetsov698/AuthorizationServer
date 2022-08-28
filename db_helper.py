import datetime
import time
from typing import Union
from models import *


# Create all DataBases
def create_all_database() -> None:
    User.create_table()
    Token.create_table()
    UserData.create_table()


# return user by username
def get_user(username: str) -> Union[User, None]:
    res = None
    try:
        res = list(User.select().where(User.username == username))[0]
    except IndexError:
        res = None
    return res


# Create and return UserData
def add_user_data(user_id, data) -> UserData:
    return UserData.create(user_id=user_id, data=data)


# return list of user_id's UserData
def get_user_data(user_id) -> list[UserData]:
    return list(UserData.select().where(UserData.user_id == user_id))


# return True if username FREE.
def check_username(username: str) -> bool:
    return len(list(User.select().where(User.username == username))) == 0


# Create user
def create_user(username: str, password: str) -> User:
    return User.create(username=username, password=password)


# Create token
def create_token(token, user_id, life_time=604800) -> Token:
    return Token.create(token=token, user_id=user_id, until_date=time.time()+life_time).token


# return True if user_id's token == token
def check_token(token, user_id) -> bool:
    if not token or not user_id:
        return False
    user_id = int(user_id)
    return len(list(Token.select().where(Token.token == token and Token.user_id == user_id))) == 1


# Delete all token, which time-life is spent
def update_tokens() -> None:
    for i in list(Token.select()):
        if time.time() > i.until_date:
            i.delete_instance()
