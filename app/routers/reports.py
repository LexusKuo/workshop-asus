import sqlite3
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/reports", tags=["reports"])


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


@router.get("/sales", response_model=None)
def sales_report(
    category: str,
    formula: Literal["total"] = Query(default="total"),
) -> object:
    connection = None
    try:
        connection = create_database()
        rows = connection.execute(
            "SELECT id, name, category, price FROM products WHERE category = ?",
            (category,),
        ).fetchall()
        total = sum(row["price"] for row in rows)
        _ = formula  # only "total" is accepted; validated by FastAPI
        return {
            "category": category,
            "items": [dict(row) for row in rows],
            "total": total,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from exc
    finally:
        if connection is not None:
            connection.close()
