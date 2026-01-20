FROM python:3.9.12-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /streaming
COPY . .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "sse:app", "--worker-class", "gevent", "--bind", "0.0.0.0:8000"]
