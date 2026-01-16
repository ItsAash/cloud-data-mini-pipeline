FROM python:3.12-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system deps (for psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Default command
CMD ["python", "main.py"]