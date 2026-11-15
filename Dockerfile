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

# Create standard UID 1000 user for Hugging Face Spaces & security
RUN useradd -m -u 1000 user || true
RUN mkdir -p uploads reports/passports data && chown -R 1000:1000 /app && chmod -R 777 /app
USER 1000

ENV PORT=7860
EXPOSE 7860 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
