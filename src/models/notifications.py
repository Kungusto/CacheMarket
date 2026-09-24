from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class NotificationsORM(BaseORM):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    title: Mapped[str]
    message: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        comment="Пользователь, который должен получить это уведомление",
    )
    payload: Mapped[dict] = mapped_column(JSONB())
