from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductDTO(BaseModel):
    product_id: int
    name: str
    description: str | None
    brand: str
    category: str
    price: Decimal
    stock_quantity: int
    created_at: datetime
    updated_at: datetime


class ProductEditDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    brand: str | None = None
    category: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None
