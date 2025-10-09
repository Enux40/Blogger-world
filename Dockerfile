# syntax=docker/dockerfile:1

# Base image
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (optional; will run at runtime too)
RUN python manage.py collectstatic --noinput || true

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=blog_proj.settings

# Cloud Run will set PORT; default to 8080
ENV PORT=8080

# Expose port
EXPOSE 8080

# Start using gunicorn; bind to 0.0.0.0:$PORT
CMD ["gunicorn", "blog_proj.wsgi:application", "--bind", "0.0.0.0:${PORT}", "--workers", "3"]
