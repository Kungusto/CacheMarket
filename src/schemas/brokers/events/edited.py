from pydantic import BaseModel


class ProductChangedEvent(BaseModel):
    product_id: int
    name: str
    changes: dict
