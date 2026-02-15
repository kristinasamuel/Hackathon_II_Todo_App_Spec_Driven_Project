# Implementation Plan: Phase-5 Cloud Deployment & Advanced Features

**Specification**: `phase-4-local-deployment/spec.md`

## **Milestones & Estimates**

| Milestone                               | Estimated Complexity | Estimated Time |
| --------------------------------------- | -------------------- | -------------- |
| M1: Intermediate Feature Implementation | L                    | 5-7 days       |
| M2: Advanced Feature Backend            | XL                   | 7-10 days      |
| M3: Dapr Integration                    | L                    | 3-5 days       |
| M4: Local Kubernetes Deployment         | M                    | 2-3 days       |
| M5: Cloud Production Deployment         | XL                   | 5-7 days       |
| M6: CI/CD Automation                    | L                    | 4-5 days       |

---

## **PHASE 1: Intermediate Features (Milestone M1)**

*Goal: Implement core task organization features (priorities, tags, search, filter, sort).*

**Task Dependencies**: This phase can start immediately.

| Task ID | Description                                                               | Dependencies |
| ------- | ------------------------------------------------------------------------- | ------------ |
| 1.1     | **DB Changes**: Write and apply Alembic migration for new columns/tables.   | -            |
| 1.2     | **API Updates**: Add `tags` endpoints to the Task service.                | 1.1          |
| 1.3     | **API Updates**: Modify `tasks` endpoints to accept/process priority.     | 1.1          |
| 1.4     | **API Updates**: Implement search, filter, and sort logic in `GET /tasks`. | 1.1          |
| 1.5     | **Validation**: Add backend validation rules for all new inputs.          | 1.2, 1.3     |
| 1.6     | **Frontend**: Implement UI for creating and managing tags.                | 1.2          |
| 1.7     | **Frontend**: Add priority selection UI to the task form.                 | 1.3          |
| 1.8     | **Frontend**: Implement search, filter, and sort controls on the task list. | 1.4          |
| 1.9     | **Testing**: Write unit/integration tests for backend changes.            | 1.5          |
| 1.10    | **Testing**: Conduct end-to-end manual testing for all new features.      | 1.8, 1.9     |

---

## **PHASE 2: Advanced Event-Driven Features (Milestone M2)**

*Goal: Implement event-driven features for recurring tasks and reminders.*

**Task Dependencies**: Requires M1 to be complete.

| Task ID | Description                                                               | Dependencies |
| ------- | ------------------------------------------------------------------------- | ------------ |
| 2.1     | **Service Creation**: Scaffold new FastAPI services: Scheduler, Reminder, Notification. | -            |
| 2.2     | **Kafka Setup**: Define Kafka topic schemas (`task-events`, `task-updates`, `reminders`). | -            |
| 2.3     | **Producers**: Modify Task Service to publish `TaskCreated`/`TaskUpdated` events. | 2.2          |
| 2.4     | **Consumers**: Implement consumer logic in Scheduler Service for recurring tasks. | 2.1, 2.3     |
| 2.5     | **Consumers**: Implement consumer logic in Reminder Service for due dates. | 2.1, 2.3     |
| 2.6     | **Consumers**: Implement consumer logic in Notification Service to process `ReminderDue` events. | 2.1, 2.5     |
| 2.7     | **Error Handling**: Implement retry/dead-letter queue strategy for all consumers. | 2.4, 2.5, 2.6|
| 2.8     | **Testing**: Write unit tests for producer and consumer logic in isolation. | 2.7          |

---

## **PHASE 3: Dapr Integration (Milestone M3)**

*Goal: Integrate Dapr sidecars to handle infrastructure concerns.*

**Task Dependencies**: Requires M2 to be complete.

| Task ID | Description                                                                       | Dependencies |
| ------- | --------------------------------------------------------------------------------- | ------------ |
| 3.1     | **Sidecar Enablement**: Add Dapr annotations to all backend service deployments.    | -            |
| 3.2     | **Pub/Sub**: Refactor event publishing/consuming logic to use the Dapr Pub/Sub API. | 2.7, 3.1     |
| 3.3     | **State Store**: Configure and test Dapr state store for the Scheduler service.     | 3.1          |
| 3.4     | **Jobs API**: Refactor Scheduler/Reminder services to use the Dapr Jobs API.        | 3.1          |
| 3.5     | **Secrets**: Configure the Dapr secret store and refactor services to use it.       | 3.1          |
| 3.6     | **Testing**: Verify all Dapr components are working correctly in a local test.      | 3.2, 3.4, 3.5|

---

## **PHASE 4: Local Deployment (Minikube) (Milestone M4)**

*Goal: Create a fully working local deployment on Minikube.*

**Task Dependencies**: Requires M3 to be complete.

| Task ID | Description                                                                          | Dependencies |
| ------- | ------------------------------------------------------------------------------------ | ------------ |
| 4.1     | **Dockerfiles**: Create/update Dockerfiles for all frontend and backend services.    | -            |
| 4.2     | **K8s Manifests**: Write basic Kubernetes manifests for all services and components. | 4.1          |
| 4.3     | **Dapr Install**: Document steps to install Dapr on Minikube.                        | -            |
| 4.4     | **Deployment Script**: Create a script to deploy all components in the correct order. | 4.2, 4.3     |
| 4.5     | **Testing Checklist**: Create and execute a checklist to validate the local deployment. | 4.4          |

---

## **PHASE 5: Cloud Deployment (AKS/GKE/OKE) (Milestone M5)**

*Goal: Deploy the application to a production-grade Kubernetes cluster.*

**Task Dependencies**: Requires M4 to be complete.

| Task ID | Description                                                                         | Dependencies |
| ------- | ----------------------------------------------------------------------------------- | ------------ |
| 5.1     | **Cluster Setup**: Provision a managed Kubernetes cluster (e.g., AKS).              | -            |
| 5.2     | **Helm Chart**: Create a Helm chart for the entire application stack.               | 4.2          |
| 5.3     | **Ingress**: Configure an Ingress controller and rules for frontend/backend.        | 5.2          |
| 5.4     | **Autoscaling**: Configure Horizontal Pod Autoscalers (HPAs) for backend services.   | 5.2          |
| 5.5     | **Secrets Management**: Set up cloud secret store and integrate with Dapr.          | 5.1          |
| 5.6     | **Environment Configs**: Finalize Helm `values.yaml` for staging and production.     | 5.2, 5.5     |
| 5.7     | **Production Validation**: Create and execute a checklist for production readiness.   | 5.6          |

---

## **PHASE 6: CI/CD Pipeline (Milestone M6)**

*Goal: Automate the build, test, and deployment process.*

**Task Dependencies**: Requires M5 to be complete.

| Task ID | Description                                                                         | Dependencies |
| ------- | ----------------------------------------------------------------------------------- | ------------ |
| 6.1     | **Workflow Design**: Outline the stages for the GitHub Actions workflow.            | -            |
| 6.2     | **Build Stage**: Implement jobs to lint, test, and build Docker images.             | 4.1          |
| 6.3     | **Push Stage**: Implement job to push tagged images to a container registry.        | 6.2          |
| 6.4     | **Deploy Stage**: Implement jobs to deploy to staging and production using Helm.    | 5.2, 6.3     |
| 6.5     | **Rollback Plan**: Document a clear rollback strategy in case of deployment failure. | 6.4          |
| 6.6     | **Testing**: Test the entire CI/CD pipeline from code push to production deployment. | 6.5          |

---

## **Deployment Flow**
1.  **Local**: `Developer Machine -> Minikube` (via `kubectl apply` or a deployment script).
2.  **Cloud**: `GitHub -> GitHub Actions -> Container Registry -> Staging (AKS/GKE) -> Production (AKS/GKE)` (via Helm).

## **General Testing Checklist**
- [ ] All database migrations apply and roll back correctly.
- [ ] All API endpoints function as per the spec.
- [ ] Event-driven flows are resilient to service failure (retries/DLQ).
- [ ] Dapr components are correctly configured and utilized.
- [ ] Local deployment on Minikube is successful and fully functional.
- [ ] CI/CD pipeline successfully deploys a change to production.
- [ ] Production environment is monitored, and logs are accessible.

## **Risk Notes**
- **Complexity**: The introduction of Kafka, Dapr, and Kubernetes at once is a significant jump in complexity. There is a high risk of integration issues. **Mitigation**: Tackle one component at a time and test integration thoroughly in the local environment (Phase 4).
- **CI/CD Flakiness**: E2E tests within the CI/CD pipeline can be flaky. **Mitigation**: Design tests for resilience and implement smart retries.
- **Cloud Costs**: Unoptimized cloud resources or unmanaged scaling can lead to unexpected costs. **Mitigation**: Set up budget alerts and perform regular cost analysis.
