# Base image: lightweight Python 3.13 build
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (respects .dockerignore)
COPY . .

# Document that the app listens on port 5000
EXPOSE 5000

# Command to run when the container starts
CMD ["python3", "flask_app.py"]
