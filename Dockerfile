# Multi-stage build for Compressor to Excel API
FROM python:3.12-slim as builder

# Install system dependencies needed for PDF processing libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

# Install runtime dependencies for PDF libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /tmp/compressor-api && \
    chown -R appuser:appuser /tmp/compressor-api

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY api/ ./api/
COPY extract_pdf_text.py .
COPY run_api.py .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Create temporary directory
RUN mkdir -p /tmp/compressor-api

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health').read()" || exit 1

# Default environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV WORKERS=4
ENV TEMP_DIR=/tmp/compressor-api

# Run the API
CMD ["sh", "-c", "uvicorn api.main:app --host ${HOST} --port ${PORT} --workers ${WORKERS}"]

