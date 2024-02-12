FROM orgoro/dlib-opencv-python:latest

# You can remove the multi-stage build if not needed

# Assuming requirements.txt is already included in orgoro/dlib-opencv-python image
# If not, you can still keep this step to install additional requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# No need for multi-stage build as you're using a pre-built image
# You can directly use the orgoro/dlib-opencv-python image

# Expose port 8000 and run your application
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]
