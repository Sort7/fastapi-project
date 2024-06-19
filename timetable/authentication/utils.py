from datetime import datetime, timedelta

import bcrypt
import jwt

from core.config import settings

# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."

#  функция передающая данные для создания jwt токена
# encoded = jwt.encode({"some": "plyload"}, private_key, algorithm="RS256")
def encode_jwt(
    payload: dict,
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
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
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

#  функция отвечающая за хеширование пароля, можно заменить одной строкой:
# hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt() # генерируем "соль"
    pwd_bytes: bytes = password.encode() # переменная лишняя можно не срздавая ее происать соответсвующее значение в следующей строке
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

