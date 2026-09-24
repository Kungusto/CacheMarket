from datetime import datetime, timezone

from pydantic import BaseModel, Field


class NotificationAddDTO(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str
    message: str
    payload: dict
    user_id: int


class NotificationDTO(NotificationAddDTO):
    notification_id: int
