# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

COPY packages ./packages

# Install the dependencies
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
RUN pip install packages/*.whl

# Install ptvsd for debugging
RUN pip install ptvsd

# Copy the project code into the container
COPY . .

# Start the server when the container launches
ENTRYPOINT ["python", "-m", "ptvsd", "--port", "3000", "--host", "0.0.0.0", "manage.py"]
