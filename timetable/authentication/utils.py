import uuid
from datetime import datetime, timedelta


import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from core.config import settings


# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login/",
)

#  функция отвечающая за хеширование пароля, можно заменить одной строкой:
# hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
def hash_password(
        password: str,
) -> str:  # -> bytes:
    salt = bcrypt.gensalt()  # генерируем "соль"
    pwd_bytes: str = password.encode()  # переменная лишняя можно не срздавая ее происать соответсвующее значение в следующей строке

    return bcrypt.hashpw(pwd_bytes, salt)


#  функция отвечающая за проверку захешированного пароля, можно заменить одной строкой:
# validate_password = bcrypt.checkpw(password.encode(), hash_password)
def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


#  функция передающая данные для создания jwt токена
# encoded = jwt.encode({"some": "plyload"}, private_key, algorithm="RS256")
def encode_jwt(
        payload: dict,
        # user_id,
        # role,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,

) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
        # user_id=user_id,
        # role=role
    )
    return encoded


#  функция отвечающая за декодирование jwt токена
#  decoded = jwt.dencode(encoded, public_key, algorithms=["RS256"])
def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded





def get_current_user(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload

#
# def get_current_auth_user(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:
#     username: str | None = payload.get("sub")
#     if user := users_db.get(username):
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="token invalid (user not found)",
#     )
#
#
# def get_current_active_auth_user(
#     user: UserSchema = Depends(get_current_auth_user),
# ):
#     if user.active:
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="user inactive",
#     )