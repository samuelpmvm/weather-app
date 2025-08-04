FROM python:3.10-slim-bullseye

# Set workdir
WORKDIR /app

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY weather_app ./weather_app

# Expose FastAPI port
EXPOSE 8000

# Set environment variable for production
ENV PYTHONUNBUFFERED=1

# Command to run the FastAPI app
CMD ["uvicorn", "weather_app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]