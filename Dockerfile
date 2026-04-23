FROM python:3.13-slim

# Install system dependencies (poppler-utils required by pdf2image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add this before the collectstatic line:
ENV SECRET_KEY=build-placeholder-not-real
ENV DEBUG=False
RUN python manage.py collectstatic --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy repo media files into the image at the volume mount point so they
# are available on first deploy (the persistent volume will overlay this
# directory at runtime, but Railway copies the image contents into an
# empty volume on first mount).
RUN mkdir -p /app/media && cp -r media/. /app/media/

CMD ["gunicorn", "portfolio.wsgi:application"]
