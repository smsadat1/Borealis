FROM python:3.12-slim 
WORKDIR /
ENV PYTHONUNBUFFERED=1

# Install dependencies

RUN apt-get update && apt-get install -y build-essential gcc && \
rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY / /app/
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -R /app

EXPOSE 8000

CMD ["/app/start.sh"]

