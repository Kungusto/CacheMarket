"""
Файл для заполнения БД огромным количеством товаров
"""
import asyncio
import random
import sys
from decimal import Decimal
from pathlib import Path

from faker import Faker

sys.path.append(str(Path(__file__).parent.parent))

from src.database import async_session_factory
from src.models.products import ProductsORM

fake = Faker()

BRANDS = ["Nike", "Adidas", "Puma", "Reebok", "New Balance"]
CATEGORIES = ["shoes", "t-shirts", "jackets", "accessories", "bags"]


async def seed(n: int = 1_000_000) -> None:
    async with async_session_factory() as session:
        products = []
        for i in range(1, n + 1):
            category = random.choice(CATEGORIES)
            brand = random.choice(BRANDS)
            products.append(
                ProductsORM(
                    name=f"{brand} {fake.word().capitalize()}",
                    description=fake.sentence(nb_words=12),
                    brand=brand,
                    category=category,
                    price=Decimal(random.randrange(500, 25_000)) / 100,
                    stock_quantity=random.randint(0, 500),
                )
            )
        session.add_all(products)
        await session.commit()
        print(f"seeded {len(products)} products")


if __name__ == "__main__":
    asyncio.run(seed())