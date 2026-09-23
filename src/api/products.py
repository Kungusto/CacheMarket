from fastapi import APIRouter

from src.api.dependencies import DBDep

router = APIRouter(prefix="/products", tags=["🛒 Товары"])


@router.get(
    path="/{product_id}",
)
async def get_product(product_id: int, db: DBDep):
    return await db.products.get_product(product_id=product_id)


@router.delete(
    path="/{product_id}",
)
async def delete_product(
    product_id: int,
    db: DBDep,
):
    await db.products.delete_product(product_id=product_id)
    await db.commit()
