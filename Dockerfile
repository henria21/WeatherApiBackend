# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY weather_app.py .

# Set environment variable for API key (overwrite at runtime with -e or .env)
ENV PYTHONUNBUFFERED=1

# Expose port 5000
EXPOSE 5000

# Run server
CMD ["python", "weather_app.py"]