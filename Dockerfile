# Multi-stage Dockerfile for Sustainable Shopping Agents

FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ ./agents/

# Create necessary directories
RUN mkdir -p logs data

# Expose ports (will be overridden by docker-compose)
EXPOSE 5001 5002 5003 5004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5001}/health || exit 1

# Default command (will be overridden by docker-compose)
CMD ["python", "agents/agent1_brand_collector.py"]

