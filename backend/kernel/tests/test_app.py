from fastapi.testclient import TestClient
from hulu_kernel.main import create_app


def test_health_and_ready():
    client = TestClient(create_app())
    assert client.get("/healthz").json()["status"] == "ok"
    assert client.get("/readyz").json() == {"status": "ready"}
