FROM python:3.11-slim-buster


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set working directory
WORKDIR /app
# Update repositories and install necessary build tools
RUN apt-get update && apt-get install -y \
    cmake \
    make \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libzbar-dev && \
    rm -rf /var/lib/apt/lists/*



# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy your project files
COPY . .

# Run Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]
