# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Ensure static directory exists inside rest-api
RUN mkdir -p rest_api/templates/static

# Expose FastAPI port
EXPOSE 8000


CMD bash -c "\
    cd transformation_dbt && \
    mkdir -p db && \
    rm -f db/dev.duckdb || true && \
    dbt clean && \
    dbt run --select 'models/' && \
    cd .. && \
    exec uvicorn rest_api.main:app --host 0.0.0.0 --port 8000"