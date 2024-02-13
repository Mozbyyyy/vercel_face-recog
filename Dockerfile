# First Stage
FROM python:3.11-slim AS builder

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

# Create a virtual environment and install dependencies
RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt

# Second Stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy the application code
COPY . .

# Set the PATH to include the virtual environment
ENV PATH="/venv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]
