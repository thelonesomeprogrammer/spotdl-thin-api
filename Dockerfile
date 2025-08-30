FROM python:3.11-slim

# Install system deps (for ffmpeg + yt-dlp inside spotdl)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create working dir
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose port
EXPOSE 5000

# Run Flask
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]

