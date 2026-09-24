from src.models.notifications import NotificationsORM
from src.repo.base import BaseRepo
from src.schemas.notifications import NotificationDTO


class NotificationRepo(BaseRepo):
    model = NotificationsORM
    schema = NotificationDTO
