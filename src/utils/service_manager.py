from src.notifications.publisher import PublisherService
from src.services.auth import AuthService
from src.services.notifications import NotificationService
from src.services.products import ProductsService
from src.utils.db_manager import DBManager


class ServiceManager:
    def __init__(self, db: DBManager):
        self.auth = AuthService(db=db)
        self.products = ProductsService(db=db, publisher_service=PublisherService())
        self.notifications = NotificationService(db=db)
