# INSTALLABLES

- [Install Docker Desktop](https://docs.docker.com/desktop/)

- [Enable Kubernetes](https://docs.docker.com/desktop/kubernetes/)

- [Install Skaffold](https://skaffold.dev/docs/install/)

- [Install Ingress Nginx](https://kubernetes.github.io/ingress-nginx/deploy/)

## RUN COMMAND
```
cd backend/
skaffold dev
```

## KUBE JOB Creation (One time run to execute db migrations.)
```
cd backend/k8s/
kubectl apply -f jobs/
```
