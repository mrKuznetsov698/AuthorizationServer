import datetime

from peewee import *


db = SqliteDatabase('db/database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField()
    username = TextField(unique=True)
    password = TextField()


class Token(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    token = TextField()
    until_date = DateTimeField()


class UserData(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    data = TextField()
    create_date = DateTimeField(default=datetime.datetime.now)
