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
    cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /api
WORKDIR /api

# Copy the requirements.txt file to the container
COPY requirements.txt /api

# Install required Python packages
RUN pip3 install -r requirements.txt

# Add the crontab file to the container
COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Expose port 8000 for the Django development server
EXPOSE 8000
