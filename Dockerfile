# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

RUN apt update && apt upgrade -y

COPY requirements.txt requirements.txt

RUN pip install --requirement requirements.txt

COPY ./flask_hws/app.py app.py
COPY ./flask_hws flask_hws

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]