import logging

from sqlalchemy import select, delete

from src.decorators.cache import cache
from src.models.products import ProductsORM
from src.repo.base import BaseRepo
from src.schemas.products import ProductDTO

log = logging.getLogger(__name__)

class ProductsRepo(BaseRepo):
    schema = ProductDTO
    model = ProductsORM

    @cache(ttl=120, key_format="product:{product_id}", stampede_protection=True)
    async def get_product(self, product_id: str) -> ProductDTO | None:
        query = (
            select(self.model)
            .filter_by(product_id=product_id)
        )
        log.info("Запрос в бд на получение товара")
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def delete_product(self, product_id: str) -> None:
        query = (
            delete(self.model)
            .filter_by(product_id=product_id)
        )
        await self.session.execute(query)
        await self.get_product.invalidate(product_id=product_id)