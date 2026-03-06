# ========================================
# STAGE 1: Builder - Cài đặt dependencies
# ========================================
FROM python:3.12.9-slim AS builder

ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Cài dependencies cần thiết cho build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy uv từ official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies vào thư mục cố định
RUN uv pip install --system --no-cache -r requirements.txt


# ========================================
# STAGE 2: Runtime - Image cuối cùng
# ========================================
FROM python:3.12.9-slim

ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Chỉ cài dependencies runtime (không build-essential, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy Python site-packages từ builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code (chỉ file cần thiết)
COPY src/ ./src/
COPY templates/ ./templates/
COPY requirements.txt .

# Tạo non-root user cho security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5678

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5678"]
