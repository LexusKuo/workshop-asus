import sqlite3
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/reports", tags=["reports"])

_ALLOWED_FORMULAS: dict[str, str] = {
    "total": "Sum of item prices",
}


def create_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price REAL)"
    )
    connection.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [
            (1, "Zenbook 14 OLED", "Laptop", 42900),
            (2, "ROG Zephyrus G14", "Gaming Laptop", 62900),
            (3, "ProArt P16", "Creator Laptop", 79900),
        ],
    )
    return connection


def _apply_formula(formula: str, total: float) -> float:
    if formula == "total":
        return total
    allowed = sorted(_ALLOWED_FORMULAS)
    raise HTTPException(status_code=422, detail=f"Unknown formula '{formula}'. Allowed: {allowed}")


@router.get("/sales", response_model=None)
def sales_report(
    category: str = Query(min_length=1, max_length=100),
    formula: Literal["total"] = Query(default="total"),
) -> object:
    connection = create_database()
    try:
        rows = connection.execute(
            "SELECT id, name, category, price FROM products WHERE category = ?",
            (category,),
        ).fetchall()
        total = sum(row["price"] for row in rows)
        calculated_total = _apply_formula(formula, total)
        return {
            "category": category,
            "items": [dict(row) for row in rows],
            "total": calculated_total,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc
    finally:
        connection.close()
