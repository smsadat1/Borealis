FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install dependencies

RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY scripts/startworker.sh .
RUN chmod +x /app/startworker.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -R /app
