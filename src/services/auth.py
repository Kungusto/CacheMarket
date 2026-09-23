import copy
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Request
from pwdlib import PasswordHash
from starlette.responses import Response

from src.config import settings
from src.exceptions.auth import (
    AccessRefreshMismatchHTTPException,
    AlreadyLoggedInHTTPException,
    InvalidRefreshTokenHTTPException,
    UnauthorizedHTTPException,
)
from src.exceptions.db import DatabaseException
from src.exceptions.users import (
    EmailAlreadyRegisteredHTTPException,
    UserNotFoundHTTPException,
    WrongPasswordHTTPException,
)
from src.schemas.auth import AuthUserSchema
from src.schemas.requests.auth import RefreshTokenHashToRevoke
from src.schemas.tokens import RefreshTokenAddDTO, RefreshTokenDTO, RefreshTokenEditDTO
from src.schemas.users import UserAddDTO, UserDTO, UserPublicSchema
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
            payload=to_encode, key=private_key, algorithm=settings.JWT_ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> dict[Any, Any]:
        return jwt.decode(
            jwt=token,
            key=settings.jwt.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.JWT_ALGORITHM],
        )


class RefreshTokenService:
    LENGTH: int = 128

    @classmethod
    def get_refresh_token(cls) -> str:
        return secrets.token_hex(cls.LENGTH // 2)

    @staticmethod
    def hash_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()


class AuthService(BaseService):
    @staticmethod
    def _set_creds_into_cookies(
        response: Response,
        access_token: str,
        refresh_token: str,
    ):
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.jwt.ACCESS_TOKEN_EXP,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=settings.jwt.REFRESH_TOKEN_EXP,
        )

    async def invalidate_refresh_token_by_hash(self, token_hash: str):
        await self.db.refresh_tokens.edit(
            self.db.refresh_tokens.model.token_hash == token_hash,
            data=RefreshTokenEditDTO(
                revoked_at=datetime.now(timezone.utc),
            ),
            exclude_unset=True,
        )

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
        await self.invalidate_refresh_token_by_hash(token_hash=hashed_token)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        await self.db.commit()
        return self.answers.OK_ANSWR

    async def update_refresh_token(
        self, curr_token: str, user_id: int, response: Response
    ):
        curr_token_hash = RefreshTokenService.hash_token(token=curr_token)
        user_session: RefreshTokenDTO = await self.db.refresh_tokens.get_filtered(
            self.db.refresh_tokens.model.token_hash == curr_token_hash, get_one=True
        )
        if user_session is None:
            raise InvalidRefreshTokenHTTPException()
        if not user_session.is_relevant:
            raise InvalidRefreshTokenHTTPException()
        if user_session.user_id != user_id:
            raise AccessRefreshMismatchHTTPException()
        await self.invalidate_refresh_token_by_hash(token_hash=curr_token_hash)
        new_refresh_token = RefreshTokenService.get_refresh_token()
        hashed_new_refresh_token = RefreshTokenService.hash_token(
            token=new_refresh_token
        )
        new_access_token = AccessTokenService.encode_token(payload={"user_id": user_id})
        await self.db.refresh_tokens.add(
            data=RefreshTokenAddDTO(
                token_hash=hashed_new_refresh_token,
                user_id=user_id,
            )
        )
        self._set_creds_into_cookies(
            response=response,
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
        await self.db.commit()
        return self.answers.OK_ANSWER

    async def _auth_user(self, response_inst: Response, user_id: int):
        access_token = AccessTokenService.encode_token(
            payload={"user_id": str(user_id)}
        )
        refresh_token = RefreshTokenService.get_refresh_token()
        hashed_refresh_token = RefreshTokenService.hash_token(token=refresh_token)
        await self.db.refresh_tokens.add(
            data=RefreshTokenAddDTO(
                token_hash=hashed_refresh_token,
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
                expires_at=datetime.now(timezone.utc)
                + timedelta(seconds=settings.jwt.REFRESH_TOKEN_EXP),
            )
        )
        self._set_creds_into_cookies(
            response=response_inst,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        await self.db.commit()

    async def register_user(self, data: AuthUserSchema, response_inst: Response):
        hashed_pwd = PasswordService.hash_password(pwd=data.password)
        try:
            user: UserDTO = await self.db.users.add(
                data=UserAddDTO(email=data.email, hashed_password=hashed_pwd)
            )
        except DatabaseException as ex:
            raise EmailAlreadyRegisteredHTTPException() from ex
        await self._auth_user(response_inst, user.user_id)
        await self.db.commit()
        return {
            "user": {
                "user_id": user.user_id,
                "email": user.email,
            },
            "status": "OK",
        }

    async def login_user(
        self, data: AuthUserSchema, request: Request, response_inst: Response
    ):
        cookies = request.cookies
        access_token = cookies.get("access_token", None)
        if access_token is not None:
            raise AlreadyLoggedInHTTPException()
        user: UserDTO = await self.db.users.get_user_by_email(email=data.email)
        if user is None:
            raise UserNotFoundHTTPException()
        verify_pwd = PasswordService.verify_password(
            hashed_pwd=user.hashed_password, pwd_to_check=data.password
        )
        if not verify_pwd:
            raise WrongPasswordHTTPException()
        await self._auth_user(response_inst, user.user_id)
        return self.answers.OK_ANSWR

    async def get_curr_user(self, user_id: int):
        user = await self.db.users.get_user_by_user_id(user_id=user_id)
        return UserPublicSchema.model_validate(user, from_attributes=True)

    async def revoke_session(self, data: RefreshTokenHashToRevoke):
        await self.invalidate_refresh_token_by_hash(
            token_hash=RefreshTokenService.hash_token(data.token_hash),
        )
        await self.db.commit()
        return self.answers.OK_ANSWR
