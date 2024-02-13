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


COPY requirements.txt requirements.txt


RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "myproject.wsgi"]
