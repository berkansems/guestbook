# Use an official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install PostgreSQL client libraries and other dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies, including psycopg
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose port 8000 to be accessible
EXPOSE 8000

# Run Django migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
