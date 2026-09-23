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
