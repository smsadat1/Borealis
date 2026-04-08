FROM python:3.12-slim 
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install dependencies

RUN apt-get update && apt-get install -y \
    gcc g++ \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY api/ ./api/
COPY rpc/ ./rpc
COPY setup/ ./setup/
COPY borealis.py .
COPY start.sh .
RUN chmod +x /app/start.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -R /app

EXPOSE 8000

CMD ["./start.sh"]

