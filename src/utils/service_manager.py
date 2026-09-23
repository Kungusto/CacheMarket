from src.services.auth import SessionsService
from src.services.users import UsersService
from src.utils.db_manager import DBManager


class ServiceManager:
    def __init__(self, db: DBManager):
        self.users = UsersService(db=db)
        self.sessions = SessionsService(db=db)