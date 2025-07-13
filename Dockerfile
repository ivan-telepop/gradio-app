FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh 

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir gradio

RUN ollama serve

CMD ["python", "main.py"]