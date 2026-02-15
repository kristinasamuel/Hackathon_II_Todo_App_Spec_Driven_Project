# Actionable Tasks: Phase-5 Cloud Deployment

This document breaks down the implementation plan into a series of actionable, dependency-ordered tasks.

**Implementation Strategy**: The feature is broken down into independently testable user stories. The recommended approach is to implement one user story at a time (MVP-first), starting with User Story 1.

**File Path Note**: File paths are specified based on the target folder structure outlined in the specification (e.g., `phase-5-cloud-deployment/k8s/...`). Per your instructions, these folders have not been created, but the tasks that create the files will need to place them in these locations.

---

## Phase 1: Foundational Tasks
*These tasks are prerequisites for all subsequent development.*

- [X] T001 Create and apply the initial database migration to add `priority`, `due_date`, `tags`, and `task_tags` tables/columns. The migration script should be located in `phase-5-cloud-deployment/backend/alembic/versions/`.

---

## Phase 2: User Story 1 - Enhanced Task Organization
*Goal: Implement core task organization features: priorities, tags, and search/filter/sort.*
*Independent Test: A user can create a task with a priority and tags, and then successfully use the filter and sort controls to find it.*

- [X] T002 [US1] Implement the `POST /api/v1/tags`, `GET /api/v1/tags`, and `DELETE /api/v1/tags/{tag_id}` endpoints in the `phase-5-cloud-deployment/backend/src/main.py` (or relevant API router file).
- [X] T003 [US1] Modify the `POST /api/v1/tasks` and `PUT /api/v1/tasks/{task_id}` endpoints to handle the `priority` and `tags` fields. This happens in `phase-5-cloud-deployment/backend/src/main.py`. (Depends on T001)
- [X] T004 [US1] Implement the search, filter, and sort logic in the `GET /api/v1/tasks` endpoint. This happens in `phase-5-cloud-deployment/backend/src/main.py`. (Depends on T001)
- [X] T005 [P] [US1] Add backend Pydantic/FastAPI validation rules for the new request bodies and query parameters in `phase-5-cloud-deployment/backend/src/models/`.
- [X] T006 [US1] Implement the frontend UI components for creating and managing tags in `phase-5-cloud-deployment/frontend_new/src/components/`. (Depends on T002)
- [X] T007 [P] [US1] Add the priority selection control to the task form component in `phase-5-cloud-deployment/frontend_new/src/components/`. (Depends on T003)
- [X] T008 [US1] Implement the UI controls for search, filter, and sort on the main task list page in `phase-5-cloud-deployment/frontend_new/src/app/`. (Depends on T004)
- [X] T009 [P] [US1] Write unit and integration tests for the new backend API endpoints and logic in `phase-5-cloud-deployment/backend/tests/`. (Depends on T002, T003, T004)
- [X] T010 [US1] Perform end-to-end manual testing of the complete task organization feature.

---

## Phase 3: User Story 2 - Recurring Tasks & Reminders
*Goal: Implement event-driven recurring tasks and reminders.*
*Independent Test: A user can create a recurring task, and a new instance of that task appears automatically after the first one is completed. A reminder is sent before the task is due.*

- [X] T011 [P] [US2] Scaffold the new FastAPI services: `Scheduler`, `Reminder`, and `Notification` in `phase-5-cloud-deployment/backend/src/`.
- [X] T012 [P] [US2] Define the Avro or JSON schemas for the Kafka topics (`task-events`, `task-updates`, `reminders`) and save them in `phase-5-cloud-deployment/kafka/schemas/`.
- [X] T013 [US2] Modify the Task Service to publish `TaskCreated` and `TaskUpdated` events to the `task-events` topic. (Depends on T012)
- [X] T014 [US2] Implement the event consumer logic in the Scheduler Service to handle recurring task scheduling. (Depends on T011, T013)
- [X] T015 [US2] Implement the event consumer logic in the Reminder Service to handle due date reminders. (Depends on T011, T013)
- [X] T016 [US2] Implement the consumer logic in the Notification Service to process `ReminderDue` events and send notifications. (Depends on T011, T015)
- [X] T017 [US2] Implement a retry and dead-letter queue (DLQ) strategy for all event consumers.
- [X] T018 [P] [US2] Write unit tests for the event producer and consumer logic in `phase-5-cloud-deployment/backend/tests/`. (Depends on T017)
- [X] T019 [US2] Perform end-to-end manual testing of the recurring tasks and reminders feature.

---

## Phase 4: Polish & Cross-Cutting Concerns

### Dapr Integration
- [X] T020 [P] Create Dapr component YAML manifest for the Kafka Pub/Sub binding in `phase-5-cloud-deployment/dapr-components/pubsub.yaml`.
- [X] T021 [P] Create Dapr component YAML manifest for the PostgreSQL State Store in `phase-5-cloud-deployment/dapr-components/statestore.yaml`.
- [X] T022 [P] Create Dapr component YAML manifest for the local Secret Store in `phase-5-cloud-deployment/dapr-components/secretstore.yaml`.
- [X] T023 Refactor all event publishing and consuming logic in all services to use the Dapr Pub/Sub API instead of a direct Kafka client. (Depends on T018, T020)
- [X] T024 Refactor the Scheduler and Reminder services to use the Dapr Jobs API for scheduling. (Depends on T014, T015)

### Local Deployment (Minikube)
- [X] T025 [P] Create/update Dockerfiles for the `frontend_new`, `backend`, `scheduler-service`, `reminder-service`, and `notification-service`.
- [X] T026 [P] Write the Kubernetes manifest for the Redpanda/Kafka StatefulSet in `phase-5-cloud-deployment/k8s/redpanda.yaml`.
- [X] T027 [P] Write the Kubernetes manifests for all backend and frontend services, including Dapr annotations, in `phase-5-cloud-deployment/k8s/`. (Depends on T025)
- [X] T028 Create a deployment script (`deploy-local.sh`) to apply the Dapr components and service manifests to Minikube in the correct order. (Depends on T027)
- [X] T029 Create and execute a testing checklist to validate the full local deployment.

### Cloud Deployment & CI/CD
- [X] T030 [P] Create the Helm chart structure in `phase-5-cloud-deployment/helm/todo-app/`.
- [X] T031 [P] Populate the Helm templates for all services based on the Kubernetes manifests in `phase-5-cloud-deployment/helm/todo-app/templates/`. (Depends on T027)
- [X] T032 Configure the Helm `values.yaml` for staging and production environments, including ingress rules, autoscaling (HPA) settings, and secret store configurations in `phase-5-cloud-deployment/helm/todo-app/`.
- [X] T033 [P] Create the GitHub Actions workflow file in `phase-5-cloud-deployment/.github/workflows/cicd.yaml`.
- [X] T034 Implement the "Lint, Test, Build" stage in the CI/CD workflow. (Depends on T033)
- [X] T035 Implement the "Push to Container Registry" stage in the CI/CD workflow. (Depends on T034)
- [X] T036 Implement the "Deploy to Staging/Production" stages using Helm in the CI/CD workflow. (Depends on T032, T035)
- [X] T037 Document the rollback strategy and test the full CI/CD pipeline.

---

## **Task Summary**

- **Total Tasks**: 37
- **Foundational Tasks**: 1
- **User Story 1 Tasks**: 9
- **User Story 2 Tasks**: 9
- **Polish & Cross-Cutting Tasks**: 18
- **Suggested MVP Scope**: Complete all tasks in the "Foundational" and "User Story 1" phases (T001 - T010).
- **Parallel Opportunities**: Tasks marked with `[P]` can potentially be worked on in parallel within their respective phases, provided their direct dependencies are met. For example, after T001 is done, tasks T002, T003, and T004 can be started simultaneously by different developers.