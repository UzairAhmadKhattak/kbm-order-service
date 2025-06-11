FROM python:3.11-slim

# Avoid interactive prompts during builds
ENV DEBIAN_FRONTEND=noninteractive

# Prevent Python from writing pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Pipfile and Pipfile.lock first for better caching
COPY Pipfile Pipfile.lock ./

# Install pipenv and dependencies
RUN pip install --upgrade pip && pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy rest of the code
COPY . .

# Expose app port
EXPOSE 8000

# Run the application
CMD ["pipenv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
