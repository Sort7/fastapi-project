from typing import Annotated

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status



from authentication.utils import decode_jwt
from core.models import db_helper
from core.schemas.user import UserSchema
from crud.users import get_user_by_token
from utils.create_token import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
        session: Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        payload: dict
):
    user = await get_user_by_token(session=session, user_id=payload.get("sub"))
    if not user == None:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )









def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

# def get_current_active_auth_user(
#     user: UserSchema = Depends(get_current_auth_user),
# ):
#     if user.active:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="inactive user",
#     )


# def validate_auth_user(
#     username: str = Form(),
#     password: str = Form(),
# ):
#     unauthed_exc = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="invalid username or password",
#     )
#     if not (user := users_db.get(username)):
#         raise unauthed_exc
#
#     if not auth_utils.validate_password(
#         password=password,
#         hashed_password=user.password,
#     ):
#         raise unauthed_exc
#
#     if not user.active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="user inactive",
#         )
#
#     return user