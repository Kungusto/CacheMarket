from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class ProductSubsORM(BaseORM):
    __tablename__ = "product_subs"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
