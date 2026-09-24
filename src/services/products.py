from src.config import settings
from src.exceptions.db import EntityAlreadyExists
from src.exceptions.product_subs import AlreadySubscribedHTTPException
from src.exceptions.products import ProductNotFoundHTTPException
from src.notifications.publisher import PublisherService
from src.schemas.brokers.enums import MessageTypesEnum
from src.schemas.brokers.events.deleted import ProductDeletedEvent
from src.schemas.brokers.events.edited import ProductChangedEvent
from src.schemas.brokers.publish import BrokerMessageSchema
from src.schemas.product_subs import ProductSubDTO
from src.schemas.products import ProductEditDTO
from src.services.base import BaseService
from src.utils.db_manager import DBManager


class ProductsService(BaseService):
    def __init__(self, db: DBManager, publisher_service: PublisherService):
        super().__init__(db=db)
        self.publisher_service = publisher_service

    async def delete_product(self, product_id: int):
        deleted_product = await self.db.products.delete_product(product_id=product_id)
        if deleted_product is None:
            raise ProductNotFoundHTTPException()
        subscribed_users = await self.db.product_subs.get_subscribed_users_by_product(
            product_id=product_id
        )
        for user_id in subscribed_users:
            await self.publisher_service.send(
                channel=settings.pub_sub.PRODUCT_EVENTS,
                message=BrokerMessageSchema(
                    user_id=user_id,
                    type=MessageTypesEnum.PRODUCT_DELETED,
                    data=ProductDeletedEvent(
                        product_id=product_id, name=deleted_product.name
                    ).model_dump(),
                ),
            )
        await self.db.commit()
        return self.answers.OK_ANSWER

    async def get_product(self, product_id: int):
        return await self.db.products.get_product(product_id=product_id)

    async def sub_on_product(self, product_id: int, user_id: int):
        product = await self.db.products.get_product(product_id=product_id)
        if product is None:
            raise ProductNotFoundHTTPException()
        try:
            await self.db.product_subs.add(
                data=ProductSubDTO(user_id=user_id, product_id=product_id)
            )
        except EntityAlreadyExists as ex:
            raise AlreadySubscribedHTTPException from ex
        await self.db.commit()
        return self.answers.OK_ANSWER

    async def edit_product(self, data: ProductEditDTO, product_id: int):
        edited_product = await self.db.products.edit(
            self.db.products.model.product_id == product_id,
            data=data,
            exclude_unset=True,
            get_one=True,
        )
        subscribed_users = await self.db.product_subs.get_subscribed_users_by_product(
            product_id=product_id
        )
        for user_id in subscribed_users:
            await self.publisher_service.send(
                channel=settings.pub_sub.PRODUCT_EVENTS,
                message=BrokerMessageSchema(
                    user_id=user_id,
                    type=MessageTypesEnum.PRODUCT_UPDATED,
                    data=ProductChangedEvent(
                        product_id=product_id,
                        changes=data.model_dump(exclude_unset=True),
                        name=edited_product.name,
                    ).model_dump(),
                ),
            )
        await self.db.commit()
        return self.answers.OK_ANSWER
