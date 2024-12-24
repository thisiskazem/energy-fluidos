FROM python:latest

# Update and install system dependencies
RUN apt update && apt install -y \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev

# Install lxml
RUN pip install lxml

# Install Prometheus client for Python
RUN pip install prometheus_client

# Set TERM environment variable to avoid errors
ENV TERM=xterm

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Copy the energy script
COPY code/energy.py .

# Make the script executable
RUN chmod +x energy.py

# Use a shell loop to run the script every minute
CMD while true; do python3 /energy.py; sleep 60; done
