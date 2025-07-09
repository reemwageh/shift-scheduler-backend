# shift-scheduler-backend/Dockerfile

FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy backend code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
