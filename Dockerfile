FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install .

CMD ["python3"]