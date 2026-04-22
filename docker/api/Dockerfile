FROM python:3.12-slim 
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install dependencies

RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY services/api/ ./api/
COPY services/rpc/ ./rpc/
COPY services/setup/ ./setup/

COPY scripts/startapiservice.sh .
RUN chmod +x /app/startapiservice.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -R /app

EXPOSE 8000

CMD ["./startapiservice.sh"]

