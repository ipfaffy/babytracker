from datetime import datetime
import re

from peewee import *  # pylint: disable=wildcard-import, unused-import, unused-wildcard-import
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from models import *
from init_db import *

app = Flask(__name__)


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


def main():
    """Main function"""
    create_db_tables()

    if not BottleType.select() and not Person.select():
        create_values()

    @app.route("/sms", methods=["POST"])
    def sms():
        resp = MessagingResponse()
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        inbound_message = request.form["Body"]
        number = request.form["From"]
        user = Person.get(phonenumber=str(number))
        logged_message = Message.create(
            sender=user, receivedat=now, raw=str(inbound_message)
        )

        pee_regex = re.compile(r"pee", flags=re.IGNORECASE)
        poop_regex = re.compile(r"poop", flags=re.IGNORECASE)
        mixed_regex = re.compile(r"mixed", flags=re.IGNORECASE)
        formula_regex = re.compile(r"formula", flags=re.IGNORECASE)
        breastmilk_regex = re.compile(r"breastmilk", flags=re.IGNORECASE)

        if formula_regex.search(inbound_message) or breastmilk_regex.search(
            inbound_message
        ):
            # TODO: Add error if not formatted correct (more than 2 entries)
            bottle_type_in_msg, bottle_amount_in_msg = inbound_message.split(" ", 1)
            bottle_type = BottleType.get(name=bottle_type_in_msg.lower())
            this_bottle = Bottle.create(
                message=logged_message,
                bottletype=bottle_type,
                quantityinoz=int(bottle_amount_in_msg),
            )
            resp.message("Logged bottle of {}.".format(bottle_type_in_msg.lower()))

        if (
            pee_regex.search(inbound_message)
            or poop_regex.search(inbound_message)
            or mixed_regex.search(inbound_message)
        ):
            # This is a diaper message
            if (
                pee_regex.search(inbound_message) and poop_regex.search(inbound_message)
            ) or mixed_regex.search(inbound_message):
                # Diaper is mixed
                diaper_contents = DiaperContentType.get(name="mixed")
            if pee_regex.search(inbound_message):
                # Diaper is only pee
                diaper_contents = DiaperContentType.get(name="pee")
            if poop_regex.search(inbound_message):
                # Diaper is only poop
                diaper_contents = DiaperContentType.get(name="poop")

            this_diaper = Diaper.create(message=logged_message)
            this_diaper_contents = DiaperContent.create(
                diaper=this_diaper, contenttype=diaper_contents
            )
            resp.message("Logged {} diaper.".format(diaper_contents.name))

        return str(resp)

    @app.route("/")
    def index():
        msg = "Hey there! You probably don't belong here."
        return msg

    app.run(host="0.0.0.0", debug=True)


main()
