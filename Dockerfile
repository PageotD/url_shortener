# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application package into the container
COPY . .

# Install the package (if you have a setup.py)
RUN pip install .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "shortener_app.main:app", "--host", "0.0.0.0", "--port", "5000", "--log-level", "info"]