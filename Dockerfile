FROM python:latest

RUN apt update
RUN apt -y install python3-lxml

COPY energy-fluidos/code/energy.py .

CMD ./energy.py
