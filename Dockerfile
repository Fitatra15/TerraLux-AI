# ========================================================
# Stage 1: Build React SPA Frontend
# ========================================================
FROM node:20-slim AS frontend-builder
WORKDIR /build

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ========================================================
# Stage 2: Python 3.10 FastAPI Backend & Static Server
# ========================================================
FROM python:3.10-slim

WORKDIR /app

# System dependencies for scientific libraries and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source code
COPY . .

# Copy compiled frontend SPA from Stage 1
COPY --from=frontend-builder /build/dist ./frontend/dist

# Ensure writable directories exist with full permissions for non-root cloud containers
RUN mkdir -p uploads reports/passports data && chmod -R 777 uploads reports data /app

ENV PORT=8000
EXPOSE 8000 7860

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
