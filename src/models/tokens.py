from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class RefreshTokensORM(BaseORM):
    __tablename__ = "refresh_tokens"

    token_hash: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
    )

