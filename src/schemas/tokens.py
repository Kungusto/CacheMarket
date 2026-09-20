from datetime import datetime

from pydantic import BaseModel


class RefreshTokenAddDTO(BaseModel):
    token_hash: str
    user_id: int
    created_at: datetime
    expires_at: datetime

class RefreshTokenDTO(RefreshTokenAddDTO):
    """Поля те же самые, создан для соблюдения узкой направленности схем"""
