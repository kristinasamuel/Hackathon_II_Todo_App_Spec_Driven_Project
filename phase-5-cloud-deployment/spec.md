# Feature Specification: Phase-5 Cloud Deployment & Advanced Features

**Feature Branch**: `N/A (Git workflow bypassed)`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Project: Todo AI Chatbot Web Application Phase: Phase-5 Cloud Deployment (Intermediate + Advanced Level Only) Context: Frontend (Next.js) and Backend (FastAPI + MCP Tools) are already fully implemented and working. Phase 1–4 are completed. Phase-5 folder already exists. Now we ONLY need specification for Intermediate and Advanced functionality + deployment architecture. No manual coding. Spec-driven workflow only. Goal: Generate a complete technical specification for Intermediate + Advanced features, local Minikube deployment, and production-grade Kubernetes cloud deployment using Kafka and Dapr."

## 1. Architecture Overview

This document specifies the architecture and implementation details for Phase 5 of the Todo AI Chatbot application. This phase introduces intermediate and advanced features, and transitions the application to a cloud-native, event-driven architecture using Kafka, Dapr, and Kubernetes.

The architecture consists of:
- **Frontend**: A Next.js single-page application.
- **Backend**: A set of FastAPI microservices.
- **Messaging**: Kafka (or Redpanda for local development) for asynchronous event-driven communication.
- **Service Mesh**: Dapr sidecars for abstracting infrastructure concerns like pub/sub, state management, and service invocation.
- **Orchestration**: Kubernetes (Minikube for local, AKS/GKE/OKE for cloud) for container orchestration.
- **CI/CD**: GitHub Actions for building, testing, and deploying the application.

## 2. User Scenarios & Testing

### User Story 1 - Enhanced Task Organization (Priority: P1)
As a user, I want to be able to set priorities and add tags to my tasks, so I can better organize and find them.

**Why this priority**: This is a foundational feature for managing a non-trivial number of tasks.
**Independent Test**: The frontend allows setting a priority and adding multiple tags during task creation and editing. The updated task properties are visible in the task list.

**Acceptance Scenarios**:
1. **Given** I am creating a new task, **When** I select a "High" priority and add tags "work" and "urgent", **Then** the task is created with that priority and those tags.
2. **Given** an existing task, **When** I edit it to change the priority to "Low" and remove the "urgent" tag, **Then** the task is updated accordingly.
3. **Given** I am viewing my task list, **When** I use the search bar with the keyword "urgent", **Then** only tasks tagged "urgent" are displayed.
4. **Given** I am viewing my task list, **When** I filter by "High" priority and status "In Progress", **Then** only tasks matching both criteria are shown.
5. **Given** I am viewing my task list, **When** I sort by "Priority", **Then** tasks are ordered from High to Low priority.

### User Story 2 - Recurring Tasks and Reminders (Priority: P2)
As a busy user, I want to create tasks that recur on a schedule and receive reminders before they are due, so I don't miss important deadlines.

**Why this priority**: Automates task management and adds proactive notifications, which is a core value proposition.
**Independent Test**: A recurring task can be created. When the next occurrence is due, a new task is automatically created in the system, and a notification is sent.

**Acceptance Scenarios**:
1. **Given** I am creating a task for "Team Standup", **When** I set it to recur daily at 9 AM and set a reminder 15 minutes before, **Then** the task is created, and I receive a notification at 8:45 AM every weekday.
2. **Given** a daily recurring task is completed today, **Then** a new task for tomorrow is automatically generated with the status "Todo".
3. **Given** a task with a due date is approaching, **When** the reminder time is reached, **Then** the notification service sends an alert to my configured channel (e.g., email, browser notification).

## 3. PART A: Intermediate Features - API and Schema

### Database Schema Updates
- **`tasks` table**:
    - Add `priority` column: `Enum("low", "medium", "high")` with a default of `'medium'`.
    - Add `due_date` column: `TIMESTAMP` (nullable).
- **`tags` table**:
    - `id`: `UUID` (Primary Key)
    - `name`: `String` (Unique, Indexed)
    - `user_id`: `UUID` (Foreign Key to `users`)
- **`task_tags` (join table)**:
    - `task_id`: `UUID` (Foreign Key to `tasks`)
    - `tag_id`: `UUID` (Foreign Key to `tags`)

### API Endpoints (Task Service)

#### **Priorities**
- No new endpoints. Priority is an attribute of a task.

#### **Tags**
- `POST /api/v1/tags`: Create a new tag.
  - **Request**: `{ "name": "work" }`
  - **Response**: `{ "id": "...", "name": "work" }`
- `GET /api/v1/tags`: List all tags for the user.
- `DELETE /api/v1/tags/{tag_id}`: Delete a tag.

#### **Task Manipulation**
- `POST /api/v1/tasks` (Update):
  - **Request Body includes**: `{ ..., "priority": "high", "tags": ["tag_id_1", "tag_id_2"] }`
- `PUT /api/v1/tasks/{task_id}` (Update):
  - **Request Body includes**: `{ ..., "priority": "low", "tags": ["tag_id_1"] }`

#### **Search, Filter, Sort**
- `GET /api/v1/tasks`:
  - **Query Parameters**:
    - `search`: string (keyword search on title and description)
    - `status`: string (e.g., "todo", "in_progress")
    - `priority`: string (e.g., "high", "medium", "low")
    - `tags`: comma-separated string of tag IDs
    - `sort_by`: string (e.g., "due_date", "priority", "created_at")
    - `order`: string ("asc" or "desc")
  - **Frontend Integration**: The frontend will construct the URL with query parameters based on user selections in the UI. When a filter or sort option is changed, the frontend re-fetches the task list with the new parameters.

## 4. PART B: Advanced Features - Event-Driven Design

### Services
1.  **Task Service**: Manages core task CRUD, publishes events on changes.
2.  **Scheduler Service**: Manages recurring task logic. Consumes task events to schedule or unschedule recurring jobs. Uses Dapr Jobs/Scheduler API.
3.  **Reminder Service**: Manages reminders. Consumes task events to schedule reminders. Uses Dapr Jobs/Scheduler API.
4.  **Notification Service**: Consumes reminder events and sends notifications to the user (e.g., via email, WebSocket).

### Kafka Topics
- `task-events`: For CRUD operations on tasks (e.g., `TaskCreated`, `TaskUpdated`, `TaskDeleted`).
- `task-updates`: For events originating from background services (e.g., `RecurringTaskInstanceCreated`).
- `reminders`: For reminder events to be processed by the Notification Service (e.g., `ReminderDue`).

### Event Schemas & Flow

**Event: `TaskCreated`**
- **Topic**: `task-events`
- **Producer**: Task Service
- **Consumers**: Scheduler Service, Reminder Service
- **Payload**: `{ "eventType": "TaskCreated", "taskId": "...", "userId": "...", "isRecurring": true, "recurrenceRule": "RRule_string", "dueDate": "...", "reminderAt": "..." }`

**Data Flow: Creating a Recurring Task**
1.  User creates a recurring task via the Frontend.
2.  Frontend sends `POST /api/v1/tasks` to the Task Service.
3.  Task Service saves the task to the database and publishes a `TaskCreated` event to the `task-events` topic via Dapr.
4.  **Scheduler Service**, subscribed to `task-events`, consumes the event. It sees `isRecurring: true`. It calls the Dapr Scheduler API to create a job that will trigger the `RecurringTaskInstanceCreated` event based on the `recurrenceRule`.
5.  **Reminder Service**, also subscribed to `task-events`, consumes the event. It sees a `dueDate` and `reminderAt`. It calls the Dapr Scheduler API to create a one-time job that will fire the `ReminderDue` event at the specified time.

## 5. PART C: Dapr Integration

### Dapr Component YAML Examples

**Pub/Sub on Kafka** (`dapr-components/pubsub-kafka.yaml`)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092" # In-cluster service name
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "todo-app"
```

**State Store (Postgres)** (`dapr-components/statestore-postgres.yaml`)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: statestore.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=postgres:5432 user=postgres password=example dbname=dapr_state"
  - name: actorStateStore
    value: "true"
```

**Secret Store** (`dapr-components/secretstore.yaml`)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: "/etc/secrets/secrets.json"
```

### Service Communication Flow
- **Service Invocation**: Frontend calls the backend gateway (Task Service) via standard HTTP. Service-to-service communication (e.g., if a new `Billing Service` needed to query the `Task Service`) would use Dapr service invocation: `http://localhost:3500/v1.0/invoke/task-service/method/api/v1/tasks/{taskId}`.
- **Publishing**: The Task Service publishes an event by POSTing to the Dapr sidecar: `POST http://localhost:3500/v1.0/publish/pubsub/task-events`. Dapr handles the interaction with Kafka.
- **Subscribing**: The Reminder Service defines an endpoint like `/reminders`. It's deployed with a Dapr Subscription declarative manifest (`dapr-components/subscription.yaml`) telling Dapr to deliver messages from the `task-events` topic to that endpoint.

## 6. PART D & E: Deployment (Local & Cloud)

### Local Deployment (Minikube)
- **Manifests**: Use basic Kubernetes manifests (`k8s/`) for simplicity.
- **Namespace**: A single `todo-app` namespace.
- **Components**:
    - `backend-deployment.yaml`: FastAPI app with Dapr annotations.
    - `frontend-deployment.yaml`: Next.js app.
    - `redpanda.yaml`: A single-node Redpanda (Kafka alternative) statefulset.
    - `postgres.yaml`: A single-node Postgres statefulset.
- **Resource Limits**: Keep resource requests/limits low (e.g., `cpu: 100m`, `memory: 128Mi`) to run on low-RAM machines.
- **Startup Order**:
    1.  Deploy Dapr to the cluster.
    2.  Deploy Postgres and Redpanda.
    3.  Deploy Dapr component manifests.
    4.  Deploy backend and frontend services.
- **Commands**: `kubectl apply -f k8s/`

### Cloud Deployment (AKS/GKE/OKE)
- **Strategy**: Use Helm charts (`helm/`) to manage the complexity of different environments (dev, staging, prod).
- **Cluster Layout**:
    - Multiple node pools (e.g., one for general services, one for stateful services like Kafka).
    - Use a managed Kubernetes service (AKS, GKE, OKE).
    - Use a managed Kafka service (e.g., Confluent Cloud) and a managed Postgres (e.g., Neon).
- **Ingress**: Use an Nginx or Traefik Ingress controller to expose the frontend and backend services.
- **Autoscaling**: Implement Horizontal Pod Autoscalers (HPA) for backend services based on CPU/memory usage or custom metrics (e.g., Kafka lag).
- **Secrets**: Use a managed secret store like Azure Key Vault, Google Secret Manager, or HashiCorp Vault, integrated via the Dapr secret store component.

### CI/CD with GitHub Actions
A workflow file in `.github/workflows/deploy.yaml` will define the pipeline:
1.  **On push to `main`**:
2.  **Lint & Test**: Run linters and unit tests for frontend and backend.
3.  **Build & Push Docker Image**: Build Docker images for each service, tag with the Git SHA, and push to a container registry (e.g., Docker Hub, ACR, GCR).
4.  **Deploy to Staging**: Use `helm upgrade --install` to deploy the new images to a staging namespace in the Kubernetes cluster.
5.  **Run Integration Tests**: Run automated tests against the staging environment.
6.  **Manual Approval**: A manual approval step before deploying to production.
7.  **Deploy to Production**: Use `helm upgrade --install` to deploy to the production namespace.

## 7. PART F: Folder Structure (For Reference)

As requested, here is the conceptual folder structure. Per your instructions, these directories have **not** been created.

- `phase-5-cloud-deployment/`
    - `spec.md` (This file)
    - `docs/` (For architecture diagrams, design documents)
    - `.github/workflows/` (For CI/CD pipeline definitions)
    - `dapr-components/` (YAML files for Dapr components)
    - `helm/` (Helm charts for cloud deployment)
        - `todo-app/`
            - `templates/`
            - `Chart.yaml`
            - `values.yaml`
    - `k8s/` (Basic manifests for local Minikube deployment)

## 8. Task Breakdown for Implementation
1.  **DB Migration**: Write an Alembic migration script to add the new tables (`tags`, `task_tags`) and columns (`priority`, `due_date`).
2.  **Backend API**: Implement the new API endpoints for tags and update the task endpoints to handle priority, filtering, and sorting.
3.  **Frontend UI**: Update the frontend components to allow setting priority, adding/removing tags, and using the new search, sort, and filter controls.
4.  **Dapr & Kafka Setup**: Write the Dapr component YAML files.
5.  **Event Integration**: Modify the backend services to publish and consume events via Dapr for the advanced features.
6.  **Create Services**: Implement the new `Scheduler`, `Reminder`, and `Notification` services.
7.  **Local K8s Manifests**: Create the `.yaml` files for all components for Minikube deployment.
8.  **Helm Chart**: Create the Helm chart for production deployment.
9.  **CI/CD Pipeline**: Write the GitHub Actions workflow for the complete CI/CD process.
