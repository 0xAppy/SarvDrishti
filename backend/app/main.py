import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.kafka.producer import producer
from app.kafka.worker import worker
from app.services.syslog_listener import start_syslog_server

from app.api.events import router as events_router
from app.api.sources import router as sources_router
from app.api.parsers import router as parsers_router
from app.api.onboarding import router as onboarding_router
from app.api.replay import router as replay_router
from app.api.stats import router as stats_router
from app.api.testing import router as testing_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await init_db()
    producer.connect()
    asyncio.create_task(worker.start_worker_loop())
    await start_syslog_server()
    yield
    # Shutdown tasks
    worker.is_running = False

app = FastAPI(
    title="SarvDrishti — Unified Log Intelligence Engine",
    version="1.0.0",
    description="SIH26156 - Enterprise Lossless Log Ingestion, Parsing, Normalization, and AI Onboarding Engine by Team Black Pearl",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats_router)
app.include_router(events_router)
app.include_router(sources_router)
app.include_router(parsers_router)
app.include_router(onboarding_router)
app.include_router(replay_router)
app.include_router(testing_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "system": "SarvDrishti — Unified Log Intelligence Engine",
        "version": "1.0.0"
    }
