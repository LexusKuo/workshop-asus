"""Regression tests for the /reports/sales endpoint (Lab 2 security remediation)."""

import pytest
from fastapi.testclient import TestClient


def test_sales_report_normal(client: TestClient) -> None:
    """Normal request returns category, matching items, and numeric total."""
    response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Laptop"
    assert isinstance(body["items"], list)
    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Zenbook 14 OLED"
    assert body["total"] == pytest.approx(42900.0)


def test_sales_report_empty_category(client: TestClient) -> None:
    """A category with no matches returns an empty items list and a zero total."""
    response = client.get("/reports/sales", params={"category": "Nonexistent"})

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Nonexistent"
    assert body["items"] == []
    assert body["total"] == pytest.approx(0.0)


def test_sales_report_sql_injection(client: TestClient) -> None:
    """SQL injection payload must not return rows from other categories."""
    payload = "' OR '1'='1"
    response = client.get("/reports/sales", params={"category": payload})

    assert response.status_code == 200
    body = response.json()
    # The injected payload does not match any real category name, so items is empty.
    assert body["items"] == []
    assert body["total"] == pytest.approx(0.0)


def test_sales_report_code_injection_rejected(client: TestClient) -> None:
    """A formula value that is not 'total' must be rejected with HTTP 422."""
    response = client.get(
        "/reports/sales",
        params={"category": "Laptop", "formula": "__import__('os').system('id')"},
    )

    assert response.status_code == 422


def test_sales_report_error_response_is_generic(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When an unexpected exception occurs, the API returns a generic error without details."""
    import app.routers.reports as reports_module

    def broken_db() -> None:
        raise RuntimeError("secret db credential xyz")

    monkeypatch.setattr(reports_module, "create_database", broken_db)

    response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 500
    body = response.json()
    # The detail must not contain internal implementation information.
    assert "xyz" not in str(body)
    assert "traceback" not in str(body).lower()
    assert body.get("detail") == "Internal server error"
