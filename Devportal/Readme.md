# DevPortal

An internal developer platform (IDP) dashboard, inspired by [Backstage](https://backstage.io/) (CNCF). DevPortal gives a single view of projects, their environments, and deployment status — backed by a GitOps pipeline.

## Architecture

```
                 ┌──────────────┐        ┌───────────────────┐
                 │   Django     │        │     FastAPI        │
                 │  (catalog)   │        │  (events service)   │
                 │  PostgreSQL  │        │     MongoDB          │
                 └──────┬───────┘        └─────────┬───────────┘
                        │ /api/*                    │ /webhooks/*, /events
                        └─────────────┬──────────────┘
                                      │
                              ┌───────▼────────┐
                              │  Dashboard UI    │
                              │ (HTML/CSS/JS)     │
                              └───────────────────┘
```

- **Django (`catalog` app)** — main application. Models: `Project`, `Environment`, `Deployment`. Exposes a REST API via Django REST Framework. Data stored in PostgreSQL.
- **FastAPI (events service)** — lightweight microservice that receives webhooks from Jenkins (build events) and ArgoCD (sync events) and stores them in MongoDB as unstructured event data.
- **Dashboard** — a dark-themed frontend that polls the Django API for project/environment/deployment status and (once built) the FastAPI service for the event log.

## GitOps pipeline

```
Terraform → Jenkins (build/test/push image) → GitOps repo (image tag commit) → ArgoCD (sync to K8s) → Prometheus/Grafana (observability)
```

- Infrastructure provisioned with **Terraform**.
- **Jenkins** builds and tests Docker images, pushes to a registry, and commits the new image tag to a separate GitOps repo.
- **ArgoCD** watches the GitOps repo and syncs manifests to Kubernetes (kubeadm-provisioned cluster).
- **Prometheus + Grafana** handle metrics and observability, surfaced on the dashboard.

Repo split:
- `myapp-source` — application code, Jenkinsfile, Terraform modules, monitoring config.
- `myapp-gitops` — per-environment Kubernetes manifests and ArgoCD application definitions.

## Tech stack

| Layer | Tech |
|---|---|
| Backend (structured data) | Django, Django REST Framework, PostgreSQL |
| Backend (event data) | FastAPI, MongoDB |
| Frontend | HTML, CSS, JavaScript |
| CI | Jenkins |
| CD | ArgoCD (GitOps) |
| Infra | Terraform, Kubernetes (kubeadm) |
| Observability | Prometheus, Grafana |

## Project status

- [x] `catalog` app: `Project`, `Environment`, `Deployment` models + Django admin
- [x] Database switched from MySQL to PostgreSQL
- [x] REST API (DRF): `/api/projects/`, `/api/environments/`, `/api/deployments/`
- [x] Dashboard frontend (polls the REST API for live status)
- [ ] FastAPI webhook microservice (Jenkins + ArgoCD events → MongoDB)
- [ ] Dockerize Django app and FastAPI service
- [ ] Terraform infrastructure
- [ ] Jenkins pipeline
- [ ] ArgoCD sync + Image Updater
- [ ] Prometheus/Grafana integration

## Local setup

### Django app

```bash
pip install -r requirements.txt

# .env
POSTGRES_DB=devportal
POSTGRES_USER=devportal_user
POSTGRES_PASSWORD=changeme
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`
- Dashboard: `http://localhost:8000/dashboard/`

### FastAPI events service *(planned)*

```bash
cd devportal-events
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

- Webhooks: `POST /webhooks/jenkins`, `POST /webhooks/argocd`
- Events: `GET /events`

## Notes

- ArgoCD only watches the Git repo, not the image registry directly — new image pushes need either a registry webhook into Jenkins (to commit the updated tag to the GitOps repo) or ArgoCD Image Updater configured to write back to Git.