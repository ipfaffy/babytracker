FROM python:3

WORKDIR /usr/src/babytracker

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD app /usr/src/babytracker/

CMD [ "python", "./app.py" ]