# Use the official Ubuntu image as the base image
FROM ubuntu:20.04

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    libpq-dev \
    netcat \
    default-mysql-client \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /api
WORKDIR /api

# Copy the requirements.txt file to the container
COPY requirements.txt /api

# Install required Python packages
RUN pip3 install -r requirements.txt

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=GTD.settings

# Expose port 8000 for the Django development server
EXPOSE 8000
