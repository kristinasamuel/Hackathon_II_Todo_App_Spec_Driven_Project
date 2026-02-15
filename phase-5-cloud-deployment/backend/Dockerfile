# Dockerfile for Backend (FastAPI application)
# Use the official Python image as a base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application code into the container
COPY . .

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Define the command to run the application
# The main application is at phase-5-cloud-deployment/backend/main.py,
# but the WORKDIR is /app, so 'main:app' should work if main.py is in the root of the copy context.
# If the entry point is within src/ for instance, it would be 'src.main:app' or 'src.api.main:app'
# Based on earlier main.py content, the actual app object is likely 'main:app'
# but it relies on imports from 'src'. So, we will ensure src is within the copied context.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
