from pydantic import BaseModel


class ProductDeletedEvent(BaseModel):
    product_id: int
    name: str
