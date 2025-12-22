FROM python:3.9.12-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /ingestion
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "main"]
