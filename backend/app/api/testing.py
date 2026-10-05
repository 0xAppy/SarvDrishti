import os
import sys
import asyncio
import subprocess
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/testing", tags=["testing"])

# Path helpers
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# Global state tracker for background live stream process
live_stream_process: Optional[subprocess.Popen] = None
live_stream_config = {
    "is_running": False,
    "delay": 1.5,
    "target_host": "127.0.0.1"
}

# Global state tracker for journalctl real system log stream
journalctl_stream_process: Optional[subprocess.Popen] = None
journalctl_stream_config = {
    "is_running": False,
    "target_host": "127.0.0.1"
}


class GenerateLogsRequest(BaseModel):
    mode: str = Field("api", description="Generation mode: file, syslog, or api")
    count: int = Field(50, description="Number of log records to generate")
    filename: str = Field("sample_historical.log", description="Filename if mode is 'file'")


class LiveStreamToggleRequest(BaseModel):
    action: str = Field(..., description="'start' or 'stop'")
    delay: float = Field(1.5, description="Delay between events in seconds")

class JournalctlStreamToggleRequest(BaseModel):
    action: str = Field(..., description="'start' or 'stop'")


@router.post("/run-tests")
async def run_pytest_suite():
    """Executes the backend pytest test suite asynchronously and returns results."""
    try:
        cmd = [sys.executable, "-m", "pytest", "tests", "-v"]
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        env["DATABASE_URL"] = "sqlite+aiosqlite:///./test_runner_sarvdrishti.db"

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=BACKEND_DIR,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        stdout, _ = await proc.communicate()
        output = stdout.decode("utf-8", errors="replace")

        # Parse test metrics from stdout output
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        skipped = output.count(" SKIPPED")

        return {
            "status": "success" if proc.returncode == 0 else "failed",
            "exit_code": proc.returncode,
            "metrics": {
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "total": passed + failed + skipped
            },
            "output": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute pytest suite: {str(e)}")


@router.post("/generate-logs")
async def generate_synthetic_logs(req: GenerateLogsRequest):
    """Executes scripts/generate_logs.py to create synthetic logs."""
    script_path = os.path.join(SCRIPTS_DIR, "generate_logs.py")
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="generate_logs.py script not found.")

    try:
        cmd = [
            sys.executable,
            script_path,
            "--mode", req.mode,
            "--count", str(req.count),
            "--file", req.filename
        ]
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=BASE_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        stdout, _ = await proc.communicate()
        output = stdout.decode("utf-8", errors="replace")

        return {
            "status": "success" if proc.returncode == 0 else "error",
            "mode": req.mode,
            "count": req.count,
            "output": output.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log generation failed: {str(e)}")


@router.get("/live-stream/status")
async def get_live_stream_status():
    """Returns the current status of the background live log stream generator."""
    global live_stream_process, live_stream_config

    is_alive = False
    if live_stream_process is not None:
        poll = live_stream_process.poll()
        if poll is None:
            is_alive = True
        else:
            live_stream_process = None

    live_stream_config["is_running"] = is_alive
    return live_stream_config


@router.post("/live-stream/toggle")
async def toggle_live_stream(req: LiveStreamToggleRequest):
    """Starts or stops the continuous live log stream generator process."""
    global live_stream_process, live_stream_config

    script_path = os.path.join(SCRIPTS_DIR, "live_stream_generator.py")
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="live_stream_generator.py not found.")

    if req.action.lower() == "start":
        # Stop existing process if already running
        if live_stream_process is not None and live_stream_process.poll() is None:
            live_stream_process.terminate()
            live_stream_process.wait()

        try:
            cmd = [
                sys.executable,
                script_path,
                "--host", "127.0.0.1",
                "--delay", str(req.delay)
            ]
            live_stream_process = subprocess.Popen(
                cmd,
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            live_stream_config["is_running"] = True
            live_stream_config["delay"] = req.delay
            return {"status": "started", "message": f"Continuous live stream started with {req.delay}s delay."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start live stream: {str(e)}")

    elif req.action.lower() == "stop":
        if live_stream_process is not None and live_stream_process.poll() is None:
            live_stream_process.terminate()
            try:
                live_stream_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                live_stream_process.kill()
            live_stream_process = None

        live_stream_config["is_running"] = False
        return {"status": "stopped", "message": "Continuous live stream stopped."}
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'.")


@router.get("/journalctl-stream/status")
async def get_journalctl_stream_status():
    """Returns the current status of the background journalctl stream generator."""
    global journalctl_stream_process, journalctl_stream_config

    is_alive = False
    if journalctl_stream_process is not None:
        poll = journalctl_stream_process.poll()
        if poll is None:
            is_alive = True
        else:
            journalctl_stream_process = None

    journalctl_stream_config["is_running"] = is_alive
    return journalctl_stream_config


@router.post("/journalctl-stream/toggle")
async def toggle_journalctl_stream(req: JournalctlStreamToggleRequest):
    """Starts or stops the continuous journalctl live log stream generator process."""
    global journalctl_stream_process, journalctl_stream_config

    script_path = os.path.join(SCRIPTS_DIR, "stream_my_real_syslog.py")
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="stream_my_real_syslog.py not found.")

    if req.action.lower() == "start":
        # Stop existing process if already running
        if journalctl_stream_process is not None and journalctl_stream_process.poll() is None:
            journalctl_stream_process.terminate()
            journalctl_stream_process.wait()

        try:
            cmd = [
                sys.executable,
                script_path,
                "--host", "127.0.0.1"
            ]
            journalctl_stream_process = subprocess.Popen(
                cmd,
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            journalctl_stream_config["is_running"] = True
            return {"status": "started", "message": f"Continuous journalctl stream started."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start journalctl stream: {str(e)}")

    elif req.action.lower() == "stop":
        if journalctl_stream_process is not None and journalctl_stream_process.poll() is None:
            journalctl_stream_process.terminate()
            try:
                journalctl_stream_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                journalctl_stream_process.kill()
            journalctl_stream_process = None

        journalctl_stream_config["is_running"] = False
        return {"status": "stopped", "message": "Continuous journalctl stream stopped."}
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'.")


@router.post("/send-real-logs")
async def send_real_system_logs():
    """Executes scripts/send_real_system_logs.py to ingest real system security events."""
    script_path = os.path.join(SCRIPTS_DIR, "send_real_system_logs.py")
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="send_real_system_logs.py not found.")

    try:
        cmd = [sys.executable, script_path, "--host", "127.0.0.1"]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=BASE_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        stdout, _ = await proc.communicate()
        output = stdout.decode("utf-8", errors="replace")

        return {
            "status": "success" if proc.returncode == 0 else "error",
            "output": output.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send real system logs: {str(e)}")
