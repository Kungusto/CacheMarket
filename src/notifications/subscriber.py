import asyncio
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))


from src.cache.redis_conn import redis_conn
from src.config import settings
from src.context.db import get_db
from src.notifications.service import NotificationHandlersService
from src.schemas.brokers.publish import BrokerMessageSchema


class NotificationsSubscriber:
    def __init__(self, notifications_service: NotificationHandlersService):
        self.notifications_service = notifications_service

    async def run(self):
        pubsub = redis_conn.pubsub()

        await pubsub.subscribe(settings.pub_sub.PRODUCT_EVENTS)

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            event_payload = json.loads(message["data"])

            await self.notifications_service.handle(
                event_payload=(BrokerMessageSchema(**event_payload))
            )


async def main():
    async with get_db() as db:
        subscriber = NotificationsSubscriber(
            notifications_service=NotificationHandlersService(db=db)
        )
    await subscriber.run()


if __name__ == "__main__":
    asyncio.run(main())
