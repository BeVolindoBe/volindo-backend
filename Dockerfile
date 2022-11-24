FROM python:alpine3.15

RUN apk update
RUN apk upgrade --available

WORKDIR /code
COPY . /code/

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
