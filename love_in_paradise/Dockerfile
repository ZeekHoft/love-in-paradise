# Use official Python base image
FROM python:3.11-slim

# Install Java (required for CoreNLP) and wget
RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r server/requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Install Stanford CoreNLP
RUN python -c "import stanza; stanza.install_corenlp()"

# Set CoreNLP home environment variable
ENV CORENLP_HOME=/root/stanza_corenlp

# Increase timeout and memory for CoreNLP
ENV CORENLP_TIMEOUT=120000
ENV JAVA_OPTS="-Xmx4g"

# Copy server code and frontend
COPY server/ ./server
COPY out/ ./out

# Expose Flask port
EXPOSE 8080

# Set the entrypoint to your server.py
CMD ["python", "server/server.py"]


