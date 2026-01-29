FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["rq", "worker", "-u", "redis://redis:6379/0", "default"]
