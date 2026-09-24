from pydantic import BaseModel

from src.schemas.brokers.enums import MessageTypesEnum, payload_schema_map


class BrokerMessageSchema(BaseModel):
    type: MessageTypesEnum
    user_id: int  # адресат
    data: dict

    def payload_schema(self) -> BaseModel:
        mapped_schema = payload_schema_map.get(self.type)
        if mapped_schema is None:
            raise ValueError("Переданного типа нет в перечне `payload_schema_map`")
        return mapped_schema
