# Local Deployment Testing Checklist

**Purpose**: Validate the successful deployment and basic functionality of the Todo AI Chatbot application on Minikube.
**Created**: 2026-02-11
**Feature**: Phase-5 Cloud Deployment - Local (Minikube)

## Setup Verification

- [ ] Minikube is running (`minikube status`).
- [ ] Dapr CLI is installed and configured.
- [ ] `kubectl` is configured to interact with Minikube (`kubectl config current-context`).
- [ ] The `todo-app` namespace exists (`kubectl get ns todo-app`).

## Infrastructure Deployment Verification

- [ ] Postgres StatefulSet and Service are running in `todo-app` namespace (`kubectl get pods -n todo-app -l app=postgres`).
- [ ] Redpanda StatefulSet and Service are running in `todo-app` namespace (`kubectl get pods -n todo-app -l app=redpanda`).
- [ ] Dapr `pubsub`, `statestore`, and `secretstore` components are deployed (`dapr components -k -n todo-app`).
- [ ] Verify Dapr sidecars are injected into application pods (check pod descriptions for Dapr containers).

## Application Deployment Verification

- [ ] All application pods are running (`kubectl get pods -n todo-app`).
  - [ ] `backend` pod is running.
  - [ ] `frontend` pod is running.
  - [ ] `scheduler-service` pod is running.
  - [ ] `reminder-service` pod is running.
  - [ ] `notification-service` pod is running.
- [ ] All application services are created (`kubectl get services -n todo-app`).

## Basic Functionality Testing

- [ ] **Frontend Access**: Access the frontend application through Minikube.
  - [ ] If using `minikube service frontend -n todo-app`, can you access the URL provided?
  - [ ] The login page loads correctly.
- [ ] **Login/Signup**:
  - [ ] Can you sign up for a new user account via the frontend?
  - [ ] Can you log in with an existing user (if you created a default user in backend init or signed up)?
  - [ ] After successful login, are you redirected to the dashboard?
- [ ] **Task CRUD (Intermediate Features)**:
  - [ ] Can you create a new task?
  - [ ] Can you assign a priority (Low, Medium, High) to a task?
  - [ ] Can you add multiple tags to a task?
  - [ ] Can you edit an existing task's title, description, priority, and tags?
  - [ ] Can you mark a task as complete?
  - [ ] Can you delete a task?
  - [ ] Can you use the search functionality to find tasks by keyword?
  - [ ] Can you use the filter functionality (by status, tag, priority) to narrow down tasks?
  - [ ] Can you sort tasks (by date, priority, created_at)?
- [ ] **Chatbot Functionality**:
  - [ ] Can you access the chatbot interface?
  - [ ] Does the chatbot respond to queries?
- [ ] **Advanced Features (Event-Driven)**: (Note: Full testing might require more setup for Kafka event monitoring)
  - [ ] Can you create a recurring task from the frontend? (Verify UI accepts recurrence rules)
  - [ ] Can you set a due date and reminder for a task?
  - [ ] Does the UI reflect that a task is recurring or has a reminder?

## Log and Status Check

- [ ] Check logs of all pods for errors (`kubectl logs <pod-name> -n todo-app`).
- [ ] Check Dapr sidecar logs for errors.

## Notes

- Remember to `eval $(minikube docker-env)` if building images directly with `docker build` for Minikube.
- Use `minikube dashboard` for a visual overview of your cluster.
