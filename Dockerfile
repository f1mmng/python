# Use a modern, supported Debian-based image for better compatibility
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

# Install your Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- CRITICAL FIXES FOR RAILWAY/PLAYWRIGHT ---

# 1. Install all necessary system dependencies for Playwright
#    This step is the most reliable way to prevent "Stopping Container" errors.
#    It requires elevated privileges (which RUN provides).
RUN playwright install-deps

# 2. Install the actual browser binaries (as part of the build, not the start)
#    This makes the container instantly runnable.
RUN playwright install chromium

# 3. Copy your application code
COPY . .

# 4. Set the final command
#    We use a shell command to ensure the script runs, 
#    and pipe the Python command's output directly.
CMD ["bash", "-c", "python main.py"]

# Note: We are now installing browsers during the BUILD phase (RUN),
# so your Railway Start Command/start.sh is no longer needed.
# The CMD line handles running the application.
