# Start with an official Python image (Debian-based)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# FIX: Create a directory for Celery Beat schedule and give ownership to appuser
RUN mkdir /app/celery_data && chown -R appuser:appgroup /app/celery_data

# Change ownership of the rest of the app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Default command for the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
