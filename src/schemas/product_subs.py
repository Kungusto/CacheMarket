from pydantic import BaseModel


class ProductSubDTO(BaseModel):
    user_id: int
    product_id: int
