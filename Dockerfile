FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cmake \
    make \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libzbar-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install face_recognition
RUN pip install dlib

COPY requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


COPY . .


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]
