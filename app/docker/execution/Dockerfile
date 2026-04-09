FROM python:3.12-slim 
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install dependencies

RUN apt-get update && apt-get install -y \
    gcc g++ \
    docker-cli \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY execution/ ./execution/
COPY rpc/ ./rpc

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -R /app

EXPOSE 8000

CMD ["python", "-m", "execution.docker_exec"]