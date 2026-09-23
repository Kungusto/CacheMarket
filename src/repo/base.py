from typing import Literal

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import overload

from src.database import BaseORM
from src.exceptions.mappers import map_integrity_error


class BaseRepo[SchemaType: BaseModel]:
    model: type[BaseORM]
    schema: type[SchemaType]

    def __init__(self, session: AsyncSession):
        self.session = session

    @overload
    async def get_filtered(
        self, *conditions, get_one: Literal[True]
    ) -> SchemaType | None: ...

    @overload
    async def get_filtered(
        self, *conditions, get_one: Literal[False]
    ) -> list[SchemaType]: ...

    async def get_filtered(
        self, *conditions, get_one: bool = False
    ) -> SchemaType | list[SchemaType] | None:
        query = select(self.model)
        if conditions:
            query = query.filter(*conditions)
        result = await self.session.execute(query)
        if get_one:
            model = result.scalar_one_or_none()
            return (
                self.schema.model_validate(model, from_attributes=True)
                if model
                else None
            )
        models = result.scalars().all()
        return [
            self.schema.model_validate(model, from_attributes=True) for model in models
        ]

    async def delete(self, *conditions, **filter_by):
        query = delete(self.model).filter(*conditions).filter_by(**filter_by)
        await self.session.execute(query)

    async def add(self, data: BaseModel) -> SchemaType:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError as ex:
            raise map_integrity_error(ex) from ex
        model = result.scalar_one_or_none()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, *conditions, data: BaseModel, exclude_unset: bool = False):
        stmt = (
            update(self.model)
            .filter(*conditions)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)
