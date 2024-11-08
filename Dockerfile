# Use Python slim base image
FROM python:3.9-slim

# Set environment variables to avoid buffering
ENV PYTHONUNBUFFERED=1

# Install dependencies for PyAudio (PortAudio)
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies, including PyAudio
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --prefer-binary duckdb

# Copy the rest of the application code
COPY . /app/

# Expose the port on which Streamlit runs (default: 8501)
EXPOSE 8080

# Run the Streamlit application
CMD ["streamlit", "run","explicit-knowledge-copilot.py", "--server.port", "8080", "--server.address", "0.0.0.0"]