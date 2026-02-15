# Dockerfile for Reminder Service
FROM python:3.10-slim-buster

WORKDIR /app/reminder-service

COPY phase-5-cloud-deployment/backend/reminder-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY phase-5-cloud-deployment/backend/reminder-service/src ./src

EXPOSE 8002 # Assuming a different port for the reminder service

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
