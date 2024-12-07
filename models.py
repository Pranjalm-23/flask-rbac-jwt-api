from mongoengine import Document, StringField

# User Model
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, choices=["admin", "user"])

# Project Model
class Project(Document):
    name = StringField(required=True)
    description = StringField()
