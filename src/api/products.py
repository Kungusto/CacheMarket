from fastapi import APIRouter

from src.api.dependencies import ServiceDep, UserIdDep
from src.schemas.products import ProductEditDTO

router = APIRouter(prefix="/products", tags=["🛒 Товары"])


@router.get(
    path="/{product_id}",
)
async def get_product(product_id: int, service: ServiceDep):
    return await service.products.get_product(product_id=product_id)


@router.delete(
    path="/{product_id}",
)
async def delete_product(product_id: int, service: ServiceDep):
    return await service.products.delete_product(product_id=product_id)


@router.patch(
    path="/{product_id}",
)
async def update_product(data: ProductEditDTO, product_id: int, service: ServiceDep):
    return await service.products.edit_product(data=data, product_id=product_id)


@router.post(path="/{product_id}/sub")
async def sub_on_product(product_id: int, service: ServiceDep, user_id: UserIdDep):
    return await service.products.sub_on_product(product_id=product_id, user_id=user_id)
