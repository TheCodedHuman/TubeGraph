# ==========================================
# STAGE 1: Builder
# ==========================================

FROM python:3.11-slim AS builder
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and utilizea virtual env in opt/ (optional folder)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Stage Separation ~~~~~~~~~~~~~~~~~~~~~~~~~

# ==========================================
# STAGE 2: Runner (Production Image)
# ==========================================

FROM python:3.11-slim
WORKDIR /app

# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN groupadd -r usergroup && useradd -r -g usergroup appuser

# Copy the virtual environment from the builder state
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY . .

# Change ownership of the application code to the non-root user
RUN chown -R appuser:usergroup /app

# Switch to the non-root user for security
USER appuser

# Initiate the application
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
