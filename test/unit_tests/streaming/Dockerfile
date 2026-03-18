FROM python:3.9-alpine3.22

ENV PYTHONUNBUFFERED=1
WORKDIR /

COPY src/streaming src/streaming
COPY test/unit_tests/streaming test/unit_tests/streaming
COPY .pylintrc .

RUN pip install -r src/streaming/requirements.txt

CMD python3 -m pylint src/ test/ --rcfile=.pylintrc && python3 -m unittest discover --verbose test/unit_tests/streaming
