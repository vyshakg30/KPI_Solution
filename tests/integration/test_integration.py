import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rest_api.main import app

DB_FILE = "transformation_dbt/db/dev.duckdb"


@pytest.fixture(scope="module")
def client():
    """Provide TestClient instance for integration tests."""
    if not os.path.exists(DB_FILE):
        pytest.fail(
            f"DuckDB file '{DB_FILE}' not found. Run dbt first to generate the database."
        )
    return TestClient(app)


def test_kpis_endpoint(client):
    """Test the /api/kpis endpoint."""
    response = client.get("/api/kpis?date=2024-01-17")
    assert response.status_code == 200

    data = response.json()
    # Correct key based on current implementation
    assert "kpis" in data
    assert isinstance(data["kpis"], list)
    # Optional: check that each item has expected keys
    if data["kpis"]:
        for item in data["kpis"]:
            for key in ["funded_at", "funded_count", "avg_apr", "principal_weighted_margin", "default_rate_D90"]:
                assert key in item


def test_alerts_endpoint(client):
    """Test the /api/alerts endpoint."""
    response = client.get("/api/alerts?date_from=2024-01-15&date_to=2024-01-17")
    assert response.status_code == 200

    data = response.json()
    # check it's a dict with expected keys
    assert isinstance(data, dict)
    assert "alerts" in data
    assert isinstance(data["alerts"], list)


def test_report_endpoint(client):
    """Test the /api/report endpoint (HTML)."""
    response = client.get("/api/report?date_from=2024-01-17&date_to=2024-01-20")
    assert response.status_code == 200

    html_content = response.text
    assert "<html" in html_content
    assert "KPI Report" in html_content
    assert "Daily Alerts" in html_content
