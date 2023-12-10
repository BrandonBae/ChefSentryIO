# Use a base image suitable for Raspberry Pi 4 and Python 3.8
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app

# Use Python to upgrade pip
RUN python3 -m ensurepip && \
    python3 -m pip install --upgrade pip

# Install Python dependencies from requirements file
RUN python3 -m pip install -r ./requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
# Copy the current directory contents into the container at /app
COPY . /app

# Environment settings to prevent Python from generating .pyc files and for unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
#CMD ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["python", "-u", "./app.py"]
