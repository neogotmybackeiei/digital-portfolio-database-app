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

CMD ["gunicorn", "portfolio.wsgi:application"]
