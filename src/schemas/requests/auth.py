from pydantic import BaseModel


class RefreshTokenHashToRevoke(BaseModel):
    token_hash: str
