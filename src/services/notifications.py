from src.services.base import BaseService


class NotificationService(BaseService):
    async def get_all_notifications(self, user_id: int):
        return await self.db.notifications.get_filtered(
            self.db.notifications.model.user_id == user_id,
        )
