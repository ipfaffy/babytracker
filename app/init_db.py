from peewee import *  # pylint: disable=wildcard-import, unused-import, unused-wildcard-import
from datetime import datetime
from models import *

def create_db_tables():
    """Creates the database tables"""
    database.create_tables(
        [Person, Message, Diaper, DiaperContent, DiaperContentType, Bottle, BottleType]
    )

def create_bottle_types():
    """Creates the needed bottle types"""
    breastmilk = BottleType(name="breastmilk")
    breastmilk.save()
    formula = BottleType(name="formula")
    formula.save()

def create_diaper_types():
    """Creates the needed diaper types"""
    poop = DiaperContentType(name="poop")
    poop.save()
    pee = DiaperContentType(name="pee")
    pee.save()
    mixed = DiaperContentType(name="mixed")
    mixed.save()

def create_people():
    """Creates the people who will be texting"""
    mike = Person(name="Mike", phonenumber="+15103422234")
    mike.save()
    jewel = Person(name="Jewel", phonenumber="+18013693155")
    jewel.save()
    karen = Person(name="Karen", phonenumber="+15102992674")
    karen.save()

def create_values():
    """Creates needed values"""
    create_bottle_types()
    create_diaper_types()
    create_people()