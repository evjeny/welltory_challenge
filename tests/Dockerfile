FROM python:3.10.1-slim-buster
WORKDIR /tests
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .