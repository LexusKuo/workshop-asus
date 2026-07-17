"""Regression tests for the /reports/sales endpoint.

These tests verify that the three confirmed vulnerabilities (SQL injection,
dynamic code execution via eval, and stack-trace disclosure) are no longer
exploitable after the Lab 2 remediation.
"""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.lab2


def test_sales_report_normal(client: TestClient) -> None:
    response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Laptop"
    assert body["total"] == 42900
    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Zenbook 14 OLED"


def test_sales_report_unknown_category_returns_empty(client: TestClient) -> None:
    response = client.get("/reports/sales", params={"category": "Unknown"})

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 0


# --- SQL injection regression tests ---


def test_sql_injection_union_is_not_exploitable(client: TestClient) -> None:
    """A classic UNION-based injection must not leak extra rows."""
    payload = "Laptop' UNION SELECT 1,'injected','Hack',0--"
    response = client.get("/reports/sales", params={"category": payload})

    assert response.status_code == 200
    for item in response.json()["items"]:
        assert item["name"] != "injected"


def test_sql_injection_tautology_does_not_return_all_rows(client: TestClient) -> None:
    """A tautology injection must not bypass the category filter."""
    payload = "' OR '1'='1"
    response = client.get("/reports/sales", params={"category": payload})

    assert response.status_code == 200
    assert response.json()["items"] == []


# --- Dynamic code execution (eval) regression tests ---


def test_formula_unknown_value_is_rejected(client: TestClient) -> None:
    """An arbitrary expression must be rejected, not evaluated."""
    payload = "__import__('os').getenv('PATH')"
    response = client.get(
        "/reports/sales", params={"category": "Laptop", "formula": payload}
    )

    assert response.status_code == 422


def test_formula_arithmetic_expression_is_rejected(client: TestClient) -> None:
    """A bare arithmetic expression that would succeed with eval must be rejected."""
    response = client.get(
        "/reports/sales", params={"category": "Laptop", "formula": "total * 2"}
    )

    assert response.status_code == 422


def test_formula_total_is_accepted(client: TestClient) -> None:
    """The only allowed formula value is 'total'."""
    response = client.get(
        "/reports/sales", params={"category": "Laptop", "formula": "total"}
    )

    assert response.status_code == 200
    assert response.json()["total"] == 42900


# --- Error disclosure regression tests ---


def test_error_response_does_not_contain_traceback(client: TestClient) -> None:
    """Server errors must not expose Python stack traces in the response body."""
    from unittest.mock import patch

    from app.routers import reports

    with patch.object(reports, "create_database", side_effect=RuntimeError("db boom")):
        response = client.get("/reports/sales", params={"category": "Laptop"})

    assert response.status_code == 500
    body_str = str(response.json())
    assert "Traceback" not in body_str
    assert "traceback" not in body_str
    assert "line " not in body_str
    assert "db boom" not in body_str
