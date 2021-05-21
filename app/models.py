from peewee import *  # pylint: disable=wildcard-import, unused-import, unused-wildcard-import
from datetime import datetime

DATABASE = '/usr/src/db/babytracker.db'

# Create a database instance that will manage the connection and
# execute queries
database = SqliteDatabase(DATABASE, pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    """a single person definition"""

    name = CharField()
    phonenumber = CharField()

class Message(BaseModel):
    """A single Message definition"""

    sender = ForeignKeyField(Person, backref="messages")
    receivedat = DateTimeField()
    raw = CharField()

class Diaper(BaseModel):
    """A single Diaper definition"""

    message = ForeignKeyField(Message, backref="diapers")

class DiaperContentType(BaseModel):
    """A single Diaper content type definition"""

    name = CharField(unique=True)

class DiaperContent(BaseModel):
    """A single Diaper Content definition"""

    diaper = ForeignKeyField(Diaper, backref="diapercontents")
    contenttype = ForeignKeyField(DiaperContentType, backref="diapercontenttypes")

class BottleType(BaseModel):
    """A Bottle Type definition"""

    name = CharField(unique=True)

class Bottle(BaseModel):
    """A Bottle definition"""

    message = ForeignKeyField(Message, backref="bottles")
    bottletype = ForeignKeyField(BottleType, backref="bottletypes")
    quantityinoz = IntegerField()