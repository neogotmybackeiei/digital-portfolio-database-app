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
 
# Provide a dummy secret key so collectstatic can run at build time
# (real SECRET_KEY is injected by Railway at runtime)
ENV SECRET_KEY=build-placeholder-not-real
ENV DEBUG=False
RUN python manage.py collectstatic --noinput
 
CMD ["gunicorn", "portfolio.wsgi:application", "--timeout", "120", "--workers", "2"]
