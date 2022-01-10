FROM python:3.10.1-slim-buster
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5336
COPY . .