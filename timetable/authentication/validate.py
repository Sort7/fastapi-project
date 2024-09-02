from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    # HTTPBearer,
    # HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel

from authentication.utils import validate_password
from crud.users import get_user_by_username

#
# async def user_validate(session: AsyncSession, username: str = Form(), password: str = Form()):
#     unauthed_exc = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="invalid username or password",
#     )
#     user = await get_user_by_username(session=session, username=username)
#     if user == None:
#         raise unauthed_exc
#     # if not (user := users_db.get(username)):
#     #     raise unauthed_exc
#
#     if not validate_password(
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