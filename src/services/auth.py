import copy
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from fastapi import Response, Request

from src.config import settings
from src.exceptions.auth import UnauthorizedHTTPException, InvalidRefreshTokenHTTPException
from src.schemas.tokens import RefreshTokenAddDTO, RefreshTokenEditDTO
from src.services.base import BaseService


class PasswordService:
    pwd_hash = PasswordHash.recommended()

    @classmethod
    def hash_password(cls, pwd: str) -> str:
        return cls.pwd_hash.hash(pwd)

    @classmethod
    def verify_password(cls, pwd_to_check: str, hashed_pwd: str) -> bool:
        return cls.pwd_hash.verify(pwd_to_check, hashed_pwd)


class AccessTokenService:
    @classmethod
    def encode_token(cls, payload: dict[Any, Any]):
        to_encode = copy.copy(payload)
        iat = datetime.now(timezone.utc)
        exp_minutes = settings.jwt.ACCESS_TOKEN_EXP
        exp = iat + timedelta(seconds=exp_minutes)
        to_encode.update({"iat": iat, "exp": exp})
        private_key = settings.jwt.PRIVATE_KEY_PATH.read_text()
        return jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=settings.JWT_ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> dict[Any, Any]:
        return jwt.decode(
            jwt=token,
            key=settings.jwt.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.JWT_ALGORITHM]
        )

class RefreshTokenService:
    LENGTH: int = 128

    @classmethod
    def get_refresh_token(cls) -> str:
        return secrets.token_hex(cls.LENGTH // 2)

    @staticmethod
    def hash_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()


class SessionsService(BaseService):
    async def get_user_sessions(self, user_id: int) -> list[RefreshTokenAddDTO]:
        return await self.db.refresh_tokens.get_filtered(
            self.db.refresh_tokens.model.user_id == user_id,
        )

    async def logout_session(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token", None)
        if refresh_token is None:
            raise UnauthorizedHTTPException()
        hashed_token = RefreshTokenService.hash_token(token=refresh_token)
        token_hash = await self.db.refresh_tokens.get_filtered(
            self.db.refresh_tokens.model.token_hash == hashed_token
        )
        if token_hash is None:
            raise InvalidRefreshTokenHTTPException()
        await self.db.refresh_tokens.edit(
            self.db.refresh_tokens.model.token_hash == hashed_token,
            data=RefreshTokenEditDTO(
                expires_at=datetime.now(timezone.utc)
            )
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"status": "OK"}