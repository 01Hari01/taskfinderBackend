# Use the official Python image as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Run the Django application using Gunicorn
CMD ["gunicorn", "djangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]
