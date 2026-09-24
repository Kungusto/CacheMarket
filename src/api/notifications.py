from fastapi import APIRouter

from src.api.dependencies import ServiceDep, UserIdDep

router = APIRouter(prefix="/notifications", tags=["🔔 Уведомления"])


@router.get(path="/")
async def get_all_notifications(service: ServiceDep, user_id: UserIdDep):
    return await service.notifications.get_all_notifications(user_id=user_id)
