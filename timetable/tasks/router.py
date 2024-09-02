from fastapi import APIRouter, Depends

from authentication.utils import http_bearer
from core.config import settings
from utils.validate_token import get_current_token_payload
from .tasks import send_email_registration

router = APIRouter(tags=["Auth"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.get("/email")
def get_dashboard_report(payload=Depends(get_current_token_payload)):
    username = payload.get("username")
    user_email = payload.get("email")
    send_email_registration.delay(username, user_email)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }