FROM python:latest

RUN mkdir "/srs"
WORKDIR /srs
COPY . /srs
RUN pip install -r requirements.txt