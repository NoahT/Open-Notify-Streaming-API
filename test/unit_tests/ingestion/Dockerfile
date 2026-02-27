FROM python:3.9-alpine3.22

ENV PYTHONUNBUFFERED=1

WORKDIR /
COPY  src/ingestion src/ingestion
COPY test/unit_tests/ingestion test/unit_tests/ingestion

RUN pip install -r src/ingestion/requirements.txt

CMD [ "python3", "-m", "unittest", "discover", "--verbose", "test/unit_tests/ingestion" ]
