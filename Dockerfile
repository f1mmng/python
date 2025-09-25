# Use a modern, supported Python image
FROM python:3.11-slim-bullseye

# Install Playwright's dependencies and browsers
RUN pip install playwright && playwright install-deps

# Set the working directory for your application
WORKDIR /app

# Copy your requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
