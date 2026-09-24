
from src.cache.redis_conn import redis_conn
from src.schemas.brokers.publish import BrokerMessageSchema


class PublisherService:
    @staticmethod
    async def send(channel: str, message: BrokerMessageSchema) -> None:
        serialized_message = message.model_dump_json()
        await redis_conn.publish(
            channel=channel,
            message=serialized_message,
        )
