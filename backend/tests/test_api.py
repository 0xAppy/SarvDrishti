import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    await init_db()

@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_stats_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "events_processed" in data
    assert "database_status" in data

@pytest.mark.asyncio
async def test_parsers_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/parsers")
    assert response.status_code == 200
    parsers = response.json()
    assert len(parsers) >= 4

@pytest.mark.asyncio
async def test_ingest_and_get_events():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Ingest event
        ingest_res = await ac.post("/api/events/ingest", json={
            "raw_payload": "SRC=10.10.1.20 DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=DENY",
            "source_id": "src-fw-test"
        })
        assert ingest_res.status_code == 200

        # Process queued messages explicitly for test harness
        from app.kafka.producer import in_memory_queue
        from app.kafka.worker import worker
        from app.db.database import AsyncSessionLocal

        while in_memory_queue:
            msg = in_memory_queue.pop(0)
            async with AsyncSessionLocal() as db:
                await worker.process_message(db, msg["raw_payload"], msg["source_id"])

        # Get events
        events_res = await ac.get("/api/events")
        assert events_res.status_code == 200
        events = events_res.json()
        assert len(events) >= 1

@pytest.mark.asyncio
async def test_ai_onboarding_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Analyze sample log
        sample = "[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL"
        analysis_res = await ac.post("/api/onboarding/analyze", json={"sample_log": sample})
        assert analysis_res.status_code == 200
        analysis = analysis_res.json()
        assert "suggested_mappings" in analysis

        proposed_id = analysis["proposed_parser_id"]
        mappings = analysis["suggested_mappings"]

        # 2. Validate proposed parser
        val_res = await ac.post("/api/onboarding/validate", json={
            "sample_log": sample,
            "parser_id": proposed_id,
            "version": "1.0.0",
            "mappings": mappings
        })
        assert val_res.status_code == 200
        assert val_res.json()["validation_status"] == "PASS"

        # 3. Approve parser
        app_res = await ac.post("/api/onboarding/approve", json={
            "parser_id": proposed_id,
            "version": "1.0.0",
            "format_name": "custom_audit",
            "mappings": mappings,
            "regex_pattern": ""
        })
        assert app_res.status_code == 200
        assert app_res.json()["status"] == "approved"

@pytest.mark.asyncio
async def test_testing_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Check live stream status
        status_res = await ac.get("/api/testing/live-stream/status")
        assert status_res.status_code == 200
        assert "is_running" in status_res.json()

        # Test log generation in file mode
        gen_res = await ac.post("/api/testing/generate-logs", json={"mode": "file", "count": 5})
        assert gen_res.status_code == 200
        assert gen_res.json()["status"] == "success"

