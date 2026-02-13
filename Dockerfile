# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/

# Copy .env
COPY .env .env

# Create raw data folder
RUN mkdir -p data/raw/matches

# Set environment variables for Python to read .env
ENV PYTHONUNBUFFERED=1

# Command to run Phase 1 ingestion
#CMD ["python", "app/fetch_matches.py"]

# Command to run Phase 2 Fetch Player Stats
CMD ["python", "app/fetch_player_stats.py"]
