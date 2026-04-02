# Self-Healing CI/CD Pipeline System

A complete CI/CD system with automatic failure detection and recovery.

## Architecture
GitHub Push → Simulated Jenkins (schedules job) → Real Jenkins (builds & tests) → Flask App → Prometheus (monitors) → Self-Healing Controller (auto-fixes failures)

## Components
- **Real Jenkins** - CI/CD pipeline (Build → Test → Deploy)
- **Flask App** - Python web app with metrics endpoint
- **Prometheus** - Monitors app health and metrics
- **Self-Healing Controller** - Detects failures and auto-restarts/retries
- **Simulated Jenkins** - Custom job scheduler with worker simulation

## How to Run
1. Start Jenkins: `net start jenkins`
2. Start Controller: `python controller/controller.py`
3. Start Prometheus: `prometheus.exe --config.file=prometheus.yml`
4. Start Simulated Jenkins: `cd simulated-jenkins && node src/server.js`

## Dashboards
- Real Jenkins: http://localhost:8080
- Simulated Jenkins: http://localhost:3000
- Prometheus: http://localhost:9090
- Flask App: http://localhost:5000