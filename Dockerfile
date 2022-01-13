FROM ubuntu:20.04

# backend system dependencies
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

CMD flask run --host 0.0.0.0