from enum import Enum

from src.schemas.brokers.events.deleted import ProductDeletedEvent
from src.schemas.brokers.events.edited import ProductChangedEvent


class MessageTypesEnum(Enum):
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"


payload_schema_map = {
    MessageTypesEnum.PRODUCT_DELETED: ProductDeletedEvent,
    MessageTypesEnum.PRODUCT_UPDATED: ProductChangedEvent,
}

assert set(MessageTypesEnum) == set(payload_schema_map)  # Проверка инварианта
