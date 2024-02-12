FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install -y \
    cmake \
    make \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libzbar-dev && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt requirements.txt


RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]



















# FROM python:3.11-slim-buster

# RUN apt-get update
# # Install opencv-python
# RUN apt-get install -y libgl1-mesa-glx libglib2.0-0 libzbar-dev && \
#     rm -rf /var/lib/apt/lists/*

# # Optional: Use a different mirror (replace with your preferred mirror)
# # RUN echo 'deb http://us.archive.ubuntu.com/ubuntu focal main restricted universe multiverse' >> /etc/apt/sources.list

# # Update repositories

# # Set working directory
# WORKDIR /app

# # Copy requirements file
# COPY requirements.txt requirements.txt

# # Install Python dependencies
# RUN pip3 install -r requirements.txt

# # Copy your project files
# COPY . .

# # Run Django with Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]


