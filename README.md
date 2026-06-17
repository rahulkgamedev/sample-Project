# Python Flask Application - Kubernetes & Jenkins Deployment

A production-ready Python Flask application with complete Kubernetes and Jenkins CI/CD pipeline setup.

## Features

- **Flask REST API** with health checks and readiness probes
- **Docker containerization** with multi-stage builds
- **Kubernetes deployment** with 3 replicas, ConfigMap, Service, Ingress, HPA
- **Jenkins CI/CD pipeline** with testing, code quality, Docker build, and K8s deployment
- **Security best practices**: Non-root user, read-only filesystem, security context, pod anti-affinity

## Prerequisites

- Python 3.11+
- Docker & Docker Hub account
- Kubernetes cluster (1.24+)
- Jenkins with kubectl and Docker plugins
- kubectl CLI configured

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Application starts at `http://localhost:5000`

## Test Endpoints

```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/info
curl -X POST http://localhost:5000/api/v1/echo -H "Content-Type: application/json" -d '{"message": "Hello"}'
```

## Docker Build & Run

```bash
docker build -t python-app:latest .
docker run -p 5000:5000 -e ENVIRONMENT="production" python-app:latest
```

## Kubernetes Deployment

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

## Jenkins Pipeline Setup

1. Create Pipeline job pointing to this repository's `Jenkinsfile`
2. Configure credentials in Jenkins:
   - `docker-username`: Docker Hub username
   - `docker-password`: Docker Hub token
3. Update image in `k8s/deployment.yaml` with your registry
4. Update hostname in `k8s/ingress.yaml`

## Pipeline Stages

1. **Checkout** - Git code checkout
2. **Build** - Python dependencies
3. **Test** - Unit tests with pytest
4. **Code Quality** - flake8 and pylint
5. **Build Docker Image** - Docker image creation
6. **Push Docker Image** - Push to registry
7. **Deploy to Kubernetes** - K8s manifests
8. **Smoke Test** - Health verification

## Project Structure

```
.
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
├── .dockerignore           # Docker exclusions
├── Jenkinsfile            # Jenkins pipeline
├── .env.example           # Environment template
├── k8s/
│   ├── namespace.yaml
│   ├── serviceaccount.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── tests/
│   ├── __init__.py
│   └── test_app.py
└── README.md
```

## Configuration

Edit `k8s/configmap.yaml` for app configuration and `k8s/deployment.yaml` for resource limits.

## Monitoring

```bash
kubectl logs -f deployment/python-app -n python-app
kubectl describe pod <pod-name> -n python-app
kubectl top pods -n python-app
```

## Troubleshooting

- **Pods not starting**: Check logs with `kubectl logs <pod-name> -n python-app`
- **Image pull errors**: Verify image is pushed and image name matches deployment.yaml
- **Ingress not working**: Ensure ingress controller is installed and hostname is resolvable
- **Probe failures**: Test endpoints with `kubectl port-forward svc/python-app 5000:80 -n python-app && curl http://localhost:5000/health`

## Security

- Non-root user (UID 1000)
- Read-only root filesystem
- No privileged capabilities
- Pod anti-affinity for distributed scheduling

## License

MIT License
