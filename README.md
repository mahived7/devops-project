# Implementation of DevOps CI/CD Pipeline for URL Health Monitoring System

A Dockerized Python/Flask URL Health Checker with a fully automated CI/CD pipeline,
cloud deployment on Render, and real-time monitoring via Prometheus.

## Live URLs
| Endpoint | Purpose |
|----------|---------|
| `/` | URL Health Checker dashboard |
| `/add` | Add a URL to monitor |
| `/delete/<id>` | Remove a monitored URL |
| `/status` | JSON API — all URL statuses |
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
│   ├── app.py           # Flask URL Health Checker application
│   └── test_app.py      # pytest automated tests
├── .github/workflows/
│   └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── docker-compose.yml   # Local Flask + Prometheus orchestration
├── prometheus.yml       # Prometheus scrape configuration
├── Dockerfile           # Container image definition
└── requirements.txt     # Python dependencies

## CI/CD Pipeline
Every push to `main` triggers automatically:
1. **Test** — pytest runs all 7 test cases
2. **Build** — Docker image is built from Dockerfile
3. **Push** — Image pushed to Docker Hub
4. **Deploy** — Render auto-deploys the new image

If any test fails, the pipeline stops — broken code never reaches production.

## How the App Works
- Add any URL to monitor (e.g. https://github.com)
- Background thread checks every URL every 30 seconds
- Dashboard shows UP/DOWN status, response time, uptime percentage
- `/status` returns live JSON data for all monitored URLs
- `/metrics` exposes Prometheus gauges per URL

## Secrets Management
All credentials stored as GitHub Secrets — never in code:

| Secret Name | Purpose |
|-------------|---------|
| `DOCKERHUB_USERNAME` | Docker Hub login |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `RENDER_DEPLOY_HOOK` | Render deployment webhook |

## Run Locally
```bash
docker compose up --build
```
- App: http://localhost:5000
- Prometheus: http://localhost:9090

## Run Tests
```bash
pytest app/test_app.py -v
```
