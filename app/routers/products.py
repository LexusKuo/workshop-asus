from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Product, ProductPage
from app.repository import get_product, list_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductPage)
def read_products(
    q: Optional[str] = Query(default=None),
    sort: Optional[Literal["name", "price"]] = Query(default=None),
    order: Literal["asc", "desc"] = Query(default="asc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=20),
) -> ProductPage:
    products = list_products()

    if q is not None:
        q_lower = q.lower()
        products = [
            p for p in products if q_lower in p.name.lower() or q_lower in p.category.lower()
        ]

    total = len(products)

    if sort is not None:
        products = sorted(products, key=lambda p: getattr(p, sort), reverse=(order == "desc"))

    start = (page - 1) * page_size
    products = products[start : start + page_size]

    return ProductPage(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
