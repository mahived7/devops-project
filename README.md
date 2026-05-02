# DevOps CI/CD Project

A production-style DevOps pipeline built from scratch — Dockerized Python app with automated CI/CD, cloud deployment, and real-time monitoring.

## Live Demo
- App: https://devops-project-gexv.onrender.com
- Health: https://devops-project-gexv.onrender.com/health
- Metrics: https://devops-project-gexv.onrender.com/metrics

## Architecture

Code Push → GitHub Actions → Run Tests (pytest) → Build Docker Image → Push to Docker Hub → Auto-Deploy on Render → Prometheus Monitoring

## Tech Stack
| Tool | Purpose |
|---|---|
| Python + Flask | Web application |
| Docker | Containerization |
| GitHub Actions | CI/CD pipeline |
| pytest | Automated testing |
| Docker Hub | Image registry |
| Render | Cloud deployment |
| Prometheus | Monitoring & metrics |

## Pipeline Flow
Every time code is pushed to `main`:
1. GitHub Actions triggers automatically
2. pytest runs all tests
3. If tests pass → Docker image is built
4. Image is pushed to Docker Hub
5. Render auto-deploys the new version
6. App is live with zero manual steps

## How to Run Locally
```bash
git clone https://github.com/mahived7/devops-project.git
cd devops-project
docker build -t devops-project .
docker run -p 5000:5000 devops-project
```
Open http://localhost:5000

## Resume Highlights
- Built end-to-end CI/CD pipeline with GitHub Actions — zero manual deployment
- Dockerized Python/Flask app deployed live on cloud (Render)
- Automated testing with pytest on every commit
- Real-time monitoring via Prometheus metrics endpoint