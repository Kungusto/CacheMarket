from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Numeric, NUMERIC, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class ProductsORM(BaseORM):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    brand: Mapped[str] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
