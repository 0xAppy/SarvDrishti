# SarvDrishti Project Setup & Execution Guide

## Prerequisites
- Operating System: Windows 11 / Linux / macOS
- Python 3.10+
- Node.js 18+ and npm
- Docker Desktop (for containerized setup)

## 1. Quick Start (Standalone Local Development)

### Backend Setup:
```bash
# Navigate to backend directory
cd backend

# Create virtual environment and install dependencies
python3 -m pip install -r requirements.txt

# Run pytest test suite
PYTHONPATH=. python3 -m pytest tests

# Start FastAPI server on port 8000
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies and start Vite dev server
npm install
npm run dev
```

The React dashboard will be accessible at: `http://localhost:3000`  
The FastAPI Swagger docs will be accessible at: `http://localhost:8000/docs`

---

## 2. Containerized Docker Setup (Production Mode)

```bash
# Build and launch all containers (Postgres, Kafka, Backend, Frontend)
docker-compose up --build -d

# Check status of containers
docker-compose ps

# Stop containers
docker-compose down
```

---

## 3. Generate Test Logs & Simulate Ingestion

```bash
# Generate sample historical log file (100 synthetic lines)
python3 scripts/generate_logs.py --mode file --count 100

# Stream synthetic Syslog datagrams to UDP 5140
python3 scripts/generate_logs.py --mode syslog --count 50

# Stream synthetic web/firewall logs to REST API
python3 scripts/generate_logs.py --mode api --count 50
```
