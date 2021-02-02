FROM python:3.9.1

RUN mkdir -p /bot-app
WORKDIR /bot-app
COPY . /bot-app
RUN pip install -r requirements.txt
