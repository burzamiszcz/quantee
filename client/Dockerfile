FROM python:3.12-slim

WORKDIR /client

COPY ./client /client

RUN pip install requests requests_toolbelt

CMD ["python", "/client/client.py"]
