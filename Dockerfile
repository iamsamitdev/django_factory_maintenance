# Dockerfile for Django Factory Maintenance System (Minebea)
# Based on: Python 3.12, Django 5.2, PostgreSQL, Pillow, psycopg2-binary, Gunicorn, Whitenoise

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=factory_maintenance.settings

# Set work directory
WORKDIR /app

# Install system dependencies for PostgreSQL and image processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        libpng-dev \
        netcat-traditional \
        && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create media directory for file uploads
RUN mkdir -p media

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Collect static files for production
RUN python manage.py collectstatic --noinput --settings=factory_maintenance.settings || true

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command: run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "factory_maintenance.wsgi:application"]