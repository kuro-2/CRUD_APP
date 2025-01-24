# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables to make Python unbuffered and set the working directory
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Copy the current directory content into the container's /app directory
COPY . /app

# Install system dependencies required for MySQL client
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    gcc \
    libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Set environment variables for Flask app (use appropriate configuration)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Set environment variables for MySQL connection (you can adjust the credentials)
ENV MYSQL_HOST=127.0.0.1
ENV MYSQL_PORT=3306
ENV MYSQL_DATABASE=emp_db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=1234

# Command to run the Flask app
CMD ["flask", "run"]
