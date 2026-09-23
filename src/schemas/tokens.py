from datetime import datetime

from pydantic import BaseModel


class RefreshTokenAddDTO(BaseModel):
    token_hash: str
    user_id: int
    created_at: datetime
    expires_at: datetime
    invoked_at: datetime | None = None

class RefreshTokenDTO(RefreshTokenAddDTO):
    """Поля те же самые, создан для соблюдения узкой направленности схем"""
    invoked_at: datetime | None

class RefreshTokenEditDTO(BaseModel):
    expires_at: datetime | None = None
    invoked_at: datetime | None = None
