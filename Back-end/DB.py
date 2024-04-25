import os
import datetime
from mongoengine import connect, Document, StringField, IntField, DateTimeField
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Connect to MongoDB
connect(os.environ['DATABASE_NAME'], host=os.environ['DATABASE_URI'])

class Student(Document):
    name = StringField(required=True)
    roll_no = IntField(required=True)
    div = StringField(required=True)
    class_no:IntField(required=True)
    en_no:IntField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Accounts(Document):
    user_id=StringField(required=True,unique=True)
    name= StringField(required=True)
    number=IntField(required=True)
    account_type=StringField(required=True)
    password=StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Attendance(Document):
    period=IntField(required=True)
    subject=StringField(required=True)
    div=StringField(required=True)
    present=[
        IntField(required=True)
    ]
    absent=[
        IntField(required=True)
    ]
    user_id=StringField(required=True)
    date=DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)
