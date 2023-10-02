# Python 3.11 Docker image
FROM python:3.11

# Set /app as working directory 
WORKDIR /app

# Copy Python requirements to container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
# Using --no-cache-dir flag to avoid caching downloaded packages on the system 
# This reduces Docker image size
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Expose port 8000 for the application
EXPOSE 8000
