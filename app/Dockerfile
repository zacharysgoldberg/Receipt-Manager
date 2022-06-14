# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

# ENV POSTGRES_DB=receipt_manager
# ENV PGUSER=postgres

RUN chmod u+x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]

# nginx image
FROM nginx:latest

COPY . /usr/share/nginx/html