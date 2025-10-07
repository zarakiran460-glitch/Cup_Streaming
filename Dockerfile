# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (example: Flask/Django)
EXPOSE 8000

# Run application (agar Flask app hai to run karega)
CMD ["python", "app.py"]
