# Use a specific version for production stability
FROM python:3.13.5-slim

# Set the working directory to /backend,
WORKDIR /backend


# NEW STEP: Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# 1. Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the entire contents of the local 'backend' folder
# This includes the app/ and frontend/ directories
COPY . .

# 3. Production Environment Variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# Ensure Python looks for modules in /backend
ENV PYTHONPATH=/backend

# 4. Run the app
# Path logic: 'app' (folder) . 'app' (file) : 'app' (FastAPI instance)
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]