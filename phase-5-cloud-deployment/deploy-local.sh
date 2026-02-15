#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

NAMESPACE="todo-app"
K8S_DIR="phase-5-cloud-deployment/k8s"
DAPR_COMPONENTS_DIR="phase-5-cloud-deployment/dapr-components"

echo "--- Deploying to Minikube ---"

# 1. Create the Kubernetes namespace if it doesn't exist
echo "1. Ensuring namespace '$NAMESPACE' exists..."
kubectl get namespace $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE
echo "Namespace '$NAMESPACE' ready."

# 2. Deploy Dapr components
echo "2. Deploying Dapr components from '$DAPR_COMPONENTS_DIR'..."
kubectl apply -f "$DAPR_COMPONENTS_DIR/pubsub.yaml" --namespace $NAMESPACE
kubectl apply -f "$DAPR_COMPONENTS_DIR/statestore.yaml" --namespace $NAMESPACE
kubectl apply -f "$DAPR_COMPONENTS_DIR/secretstore.yaml" --namespace $NAMESPACE
echo "Dapr components deployed."

# 3. Deploy Infrastructure (Postgres and Redpanda)
echo "3. Deploying infrastructure (Postgres, Redpanda) from '$K8S_DIR'..."
kubectl apply -f "$K8S_DIR/postgres.yaml" --namespace $NAMESPACE
kubectl apply -f "$K8S_DIR/redpanda.yaml" --namespace $NAMESPACE
echo "Waiting for Postgres and Redpanda to be ready..."
kubectl wait --namespace $NAMESPACE 
  --for=condition=ready pod -l app=postgres 
  --timeout=300s
kubectl wait --namespace $NAMESPACE 
  --for=condition=ready pod -l app=redpanda 
  --timeout=300s
echo "Postgres and Redpanda are ready."

# 4. Deploy Application Services (Backend, Frontend, Scheduler, Reminder, Notification)
echo "4. Deploying application services from '$K8S_DIR'..."
kubectl apply -f "$K8S_DIR/backend-deployment.yaml" --namespace $NAMESPACE
kubectl apply -f "$K8S_DIR/frontend-deployment.yaml" --namespace $NAMESPACE
kubectl apply -f "$K8S_DIR/scheduler-deployment.yaml" --namespace $NAMESPACE
kubectl apply -f "$K8S_DIR/reminder-deployment.yaml" --namespace $NAMESPACE
kubectl apply -f "$K8S_DIR/notification-deployment.yaml" --namespace $NAMESPACE
echo "Application services deployed."

echo "--- Deployment to Minikube complete! ---"
echo "You can check the status with: kubectl get all -n $NAMESPACE"
echo "To access the frontend locally, you might need to use 'minikube service frontend -n $NAMESPACE'"
