# Dockerfile for Scheduler Service
FROM python:3.10-slim-buster

WORKDIR /app/scheduler-service

COPY phase-5-cloud-deployment/backend/scheduler-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY phase-5-cloud-deployment/backend/scheduler-service/src ./src

EXPOSE 8001 # Assuming a different port for the scheduler service

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
