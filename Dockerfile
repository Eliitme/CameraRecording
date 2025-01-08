# Use a smaller base image for Python
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies for ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    cron \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Install Python dependencies (if any, add requirements.txt to project)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy only the necessary files (to keep image efficient)
COPY multi_rtsp_recording.py /app/
COPY cleanup_old_files.py /app/
COPY flask_app.py /app/
COPY config.json /app/

COPY crontab /etc/cron.d/cleanup-cron

# Set proper permissions for the crontab file
RUN chmod 0644 /etc/cron.d/cleanup-cron

# Create the recordings folder
FROM base AS final
# Expose port (optional, if you plan to use web services)
WORKDIR /app
EXPOSE 8080

# Set the command to run both the recording and cleanup scripts in parallel
CMD ["bash", "-c", "cron && python3 multi_rtsp_recording.py && python3 flask_app.py && python3 cleanup_old_files.py"]
