# ./api1/llm/Dockerfile (With torch install)
FROM python:3.11-slim

# Install minimal system dependencies (if any needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy and install dependencies (install torch from CPU index)
COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5050

# Default command to start the Flask server
CMD ["python", "app.py", "--mode", "server"]