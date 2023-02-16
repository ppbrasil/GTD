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

# Add cron job
COPY crontab /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN crontab /etc/cron.d/my-cron

# Install required Python packages
RUN pip3 install -r requirements.txt

# Expose port 8000 for the Django development server
EXPOSE 8000
