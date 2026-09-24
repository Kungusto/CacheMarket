
from src.schemas.brokers.enums import MessageTypesEnum
from src.schemas.brokers.events.deleted import ProductDeletedEvent
from src.schemas.brokers.events.edited import ProductChangedEvent
from src.schemas.brokers.publish import BrokerMessageSchema
from src.schemas.notifications import NotificationAddDTO
from src.utils.db_manager import DBManager


class NotificationHandlersService:
    def __init__(self, db: DBManager):
        self.db = db

        self._handle_map = {
            MessageTypesEnum.PRODUCT_DELETED: self._handle_product_deletion,
            MessageTypesEnum.PRODUCT_UPDATED: self._handle_product_changing,
        }

        # Проверка, что обработка каждого из видов сообщений реализована
        assert set(self._handle_map) == set(MessageTypesEnum)

    async def handle(self, event_payload: BrokerMessageSchema):
        message_schema_cls = event_payload.payload_schema()
        message_schema = message_schema_cls.model_validate(event_payload.data)
        handler = self._handle_map.get(event_payload.type)
        await handler(message_schema, event_payload.user_id)

    async def _handle_product_deletion(
        self, message_meta: ProductDeletedEvent, user_id: int
    ):
        await self.db.notifications.add(
            data=NotificationAddDTO(
                title="Удаление товара",
                message=f"Товар {message_meta.name!r} был удален",
                payload={"product_id": message_meta.product_id},
                user_id=user_id,
            )
        )
        await self.db.commit()

    async def _handle_product_changing(
        self, message_meta: ProductChangedEvent, user_id: int
    ):
        await self.db.notifications.add(
            data=NotificationAddDTO(
                title="Изменение товара",
                message=f"Товар {message_meta.name!r} был изменен",
                payload={"changes": message_meta.changes},
                user_id=user_id,
            )
        )
        await self.db.commit()
