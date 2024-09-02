from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer


from app.config.enviroment import Settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:
    def __init__(self):
        pass

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"expire": str(expire)})
        encoded_jwt = jwt.encode(
            to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
        )
        return encoded_jwt
