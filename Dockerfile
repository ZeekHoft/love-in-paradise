# Use official Python base image
FROM python:3.11-slim

# Install Java (required for CoreNLP) and wget
RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Install Stanford CoreNLP
RUN python -c "import stanza; stanza.install_corenlp()" || echo "CoreNLP will install on first use"

# Set CoreNLP environment variables
ENV CORENLP_HOME=/root/stanza_corenlp
ENV CORENLP_TIMEOUT=180000
ENV JAVA_OPTS="-Xmx3g"
ENV PYTHONUNBUFFERED=1

# Copy entire server directory
COPY server/ .

# Copy frontend
COPY out/ ./out/

# Expose Flask port
EXPOSE 8080

# Create startup script that starts CoreNLP server AND Flask
RUN echo '#!/bin/bash\n\
set -e\n\
echo "=== Starting Fact Checker Application ==="\n\
echo "Python version: $(python --version)"\n\
echo "Working directory: $(pwd)"\n\
echo ""\n\
echo "Starting CoreNLP server in background..."\n\
cd $CORENLP_HOME\n\
nohup java -Xmx3g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 180000 > /tmp/corenlp.log 2>&1 &\n\
CORENLP_PID=$!\n\
echo "CoreNLP server started with PID: $CORENLP_PID"\n\
echo "Waiting for CoreNLP to be ready..."\n\
for i in {1..30}; do\n\
  if curl -s http://localhost:9000/ > /dev/null 2>&1; then\n\
    echo "CoreNLP is ready!"\n\
    break\n\
  fi\n\
  echo "Waiting for CoreNLP... ($i/30)"\n\
  sleep 2\n\
done\n\
cd /app\n\
echo ""\n\
echo "Starting Flask server..."\n\
python -u server.py\n' > /app/start.sh && chmod +x /app/start.sh

CMD ["/bin/bash", "/app/start.sh"]