FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .