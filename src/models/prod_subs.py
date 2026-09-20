from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class ProductSubscriptionsORM(BaseORM):
    __tablename__ = "prod_subs"
    __table_args__ = {
        "comment": "Подписки пользователей на информацию о товарах"
    }
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id", ondelete="CASCADE"),
        primary_key=True
    )
