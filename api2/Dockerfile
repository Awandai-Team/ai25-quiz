FROM python:3-alpine
# Install necessary tools
RUN apk add --no-cache shadow bash

# Create home directory and logs directory
RUN mkdir -p /app /logs

# Create user with home directory and password
RUN useradd -m -d /app awandai && \
    echo "awandai:awandai" | chpasswd
RUN chown -R awandai /app
RUN chown -R awandai /logs
# Switch to the new user (optional, depending on container purpose)
USER awandai

# Set working directory to /app
WORKDIR /app
COPY . .

# Additional packages ...
# RUN apk --help
# Default command (optional)
# CMD ["sh"]

# Install Python required packages: pipenv fastapi[standard] pydantic
RUN python3 -m pip install -r /app/requirements.txt

# Expose default FastAPI port
EXPOSE 8000

# Set entrypoint to run FastAPI in dev mode
#   python -m fastapi dev api2_simple.py
ENTRYPOINT ["python", "-m", "fastapi", "dev", "api2_simple.py"]
