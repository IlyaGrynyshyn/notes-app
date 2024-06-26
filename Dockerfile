FROM python:3.10.0-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user


RUN chown -R django-user:django-user .
RUN chmod -R 755 .

USER django-user


