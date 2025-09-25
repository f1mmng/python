# Use a newer, supported Debian-based image. Bullseye is a good choice.
FROM python:3.11-slim-bullseye

# Install Playwright's required system dependencies.
# The `playwright install-deps` command provides the canonical list.
# We run it here to ensure everything is installed correctly.
RUN pip install playwright && playwright install-deps

# Set the working directory for your application
WORKDIR /app

# Copy your requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python code into the container
COPY . .

# Tell the container what command to run when it starts
CMD ["python", "main.py"]
