FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY src/orchestrator_v2/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Set PYTHONPATH to include /app/src
ENV PYTHONPATH=/app/src

# Run the application
CMD ["python", "-m", "orchestrator_v2.main_fastapi"]
