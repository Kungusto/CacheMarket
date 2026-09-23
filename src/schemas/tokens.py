from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field

from src.config import settings


class RefreshTokenAddDTO(BaseModel):
    token_hash: str
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(timezone.utc)
            + timedelta(seconds=settings.jwt.REFRESH_TOKEN_EXP)
        )
    )
    revoked_at: datetime | None = None


class RefreshTokenDTO(RefreshTokenAddDTO):
    """Поля те же самые, создан для соблюдения узкой направленности схем"""

    revoked_at: datetime | None

    @property
    def is_relevant(self) -> bool:
        now = datetime.now(timezone.utc)
        is_not_invoked = self.revoked_at is None or now < self.revoked_at
        is_not_expired = now < self.expires_at
        return is_not_invoked and is_not_expired


class RefreshTokenEditDTO(BaseModel):
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
