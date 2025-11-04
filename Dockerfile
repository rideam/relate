# Build stage
FROM python:3.12-slim AS builder

# Copy uv from official distroless image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install build dependencies including Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmemcached-dev \
    git \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install frontend dependencies first (better layer caching)
COPY package.json package-lock.json rollup.config.mjs ./
RUN npm ci --production=false

# Copy Python dependency files for better layer caching
COPY pyproject.toml uv.lock README.rst ./

# Set uv environment variables for optimal Docker builds
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Install Python dependencies using uv (without project itself for better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --extra postgres

# Copy source code
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --extra postgres

# Build frontend assets
RUN npm run build && \
    npm prune --production && \
    rm -rf node_modules/.cache

# Production stage
FROM python:3.12-slim AS production

# Copy uv from official distroless image (optional in production if using only the venv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH="/app/.venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libpq5 \
    libmemcached11 \
    xmlsec1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user early
RUN useradd --create-home --shell /bin/bash --uid 1000 relate

# Set working directory and create required directories
WORKDIR /app
RUN mkdir -p git-roots bulk-storage static && \
    chown -R relate:relate git-roots bulk-storage static

# Copy the virtual environment from builder
COPY --from=builder --chown=relate:relate /app/.venv /app/.venv

# Copy application code
COPY --chown=relate:relate . .

# Copy built frontend assets from builder stage
COPY --from=builder --chown=relate:relate /app/frontend-dist /app/frontend-dist/

# Copy MathJax from builder stage (needed for STATICFILES_DIRS)
COPY --from=builder --chown=relate:relate /app/node_modules/mathjax /app/node_modules/mathjax

# Remove unnecessary files to reduce image size
RUN find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true && \
    find . -name "*.pyc" -delete && \
    find . -name "*.pyo" -delete && \
    rm -rf .git .github tests/ docs/ *.md Dockerfile* docker-compose* .env* && \
    chown -R relate:relate /app

# Switch to non-root user
USER relate

# Health check
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/', timeout=10)" || exit 1

# Expose port
EXPOSE 8000

# Use exec form for better signal handling
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
