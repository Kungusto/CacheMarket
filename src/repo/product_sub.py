from collections.abc import Iterable

from sqlalchemy import select

from src.models import ProductSubsORM
from src.repo.base import BaseRepo
from src.schemas.product_subs import ProductSubDTO


class ProductSubsRepo(BaseRepo):
    schema = ProductSubDTO
    model = ProductSubsORM

    async def get_subscribed_users_by_product(self, product_id: int) -> Iterable[int]:
        stmt = select(self.model.user_id).filter_by(product_id=product_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
