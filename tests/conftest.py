"""Shared fixtures: an API client and a live server for Playwright UI tests."""
import socket
import threading
import time

import pytest
import uvicorn
from fastapi.testclient import TestClient

from app.main import app, reset_state


@pytest.fixture(autouse=True)
def _clean_state():
    reset_state()
    yield


@pytest.fixture
def api():
    return TestClient(app)


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def live_server():
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)
