# Dockerfile for Notification Service
FROM python:3.10-slim-buster

WORKDIR /app/notification-service

COPY phase-5-cloud-deployment/backend/notification-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY phase-5-cloud-deployment/backend/notification-service/src ./src

EXPOSE 8003 # Assuming a different port for the notification service

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]
