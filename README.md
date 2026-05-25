# DevOps CI/CD Project

A Dockerized Python/Flask Task Manager with a fully automated CI/CD pipeline,
cloud deployment on Render, and real-time monitoring via Prometheus.

## Live URLs
| Endpoint | Purpose |
|----------|---------|
| `/` | Task Manager app |
| `/health` | Health check (JSON) |
| `/metrics` | Prometheus metrics |

## Tech Stack
- **App:** Python, Flask
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Testing:** pytest
- **Registry:** Docker Hub
- **Deployment:** Render
- **Monitoring:** Prometheus

## Project Structure
devops-project/
├── app/
│   ├── app.py           # Flask application
│   └── test_app.py      # pytest tests
├── .github/workflows/
│   └── ci-cd.yml        # GitHub Actions pipeline
├── docker-compose.yml   # Local dev with Prometheus
├── prometheus.yml       # Prometheus scrape config
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies

## CI/CD Pipeline
Every push to `main` triggers:
1. **Test** — pytest runs all tests automatically
2. **Build** — Docker image is built
3. **Push** — Image pushed to Docker Hub
4. **Deploy** — Render auto-deploys the new image

If tests fail, the pipeline stops — broken code never reaches production.

## Secrets Management
All sensitive credentials are stored as **GitHub Secrets** —
never hardcoded in code.

| Secret Name | What it stores |
|-------------|---------------|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `RENDER_DEPLOY_HOOK` | Render deployment webhook URL |

These are referenced in the GitHub Actions workflow as:
```yaml
${{ secrets.DOCKERHUB_USERNAME }}
${{ secrets.DOCKERHUB_TOKEN }}
${{ secrets.RENDER_DEPLOY_HOOK }}
```
Secrets are encrypted by GitHub, never visible in logs,
and never exposed in the repository.

## Run Locally with Docker Compose
```bash
docker-compose up --build
```
- App: http://localhost:5000
- Prometheus: http://localhost:9090

## Run Tests
```bash
pytest app/test_app.py -v
```