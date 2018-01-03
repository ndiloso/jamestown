from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField, PrimaryKeyField

from datetime import datetime

class PlaceModel(BaseModel):
	ID = PrimaryKeyField()
	NameOfPlace = CharField(200)
	Description = TextField()
	GPS = CharField(150)
	PhotoPlace = CharField(150)
	PhotoQrcode = CharField(150)
	PhoneNumberPlace1 = CharField(50)
	PhoneNumberPlace2 = CharField(50)

class UserModel(BaseModel):
	ID = PrimaryKeyField()
	NameOfUser = CharField(50)
	Email = CharField(50)
	Password = CharField(250)
	DateCreated = DateTimeField(default=datetime.now)

