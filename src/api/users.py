from fastapi import APIRouter, Response, Request

from src.api.dependencies import ServiceDep
from src.schemas.auth import AuthUserSchema

router = APIRouter(prefix="/auth", tags=["👥 Пользователи"])

@router.post(
    path="/register"
)
async def register_user(
    data: AuthUserSchema,
    response: Response,
    service: ServiceDep
):
    return await service.users.register_user(data=data, response_inst=response)


@router.post(
    path="/login"
)
async def login_user(
    data: AuthUserSchema,
    service: ServiceDep,
    request: Request,
    response_inst: Response
):
    return await service.users.login_user(
        data=data,
        request=request,
        response_inst=response_inst
    )
