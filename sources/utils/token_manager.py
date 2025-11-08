from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from core import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(BaseModel):
    sub: Optional[str | int] = None
    exp: int
    email: str = None
    phone_number: str = None
    purpose: str = None
    type: str = None
    role: str = None


class TokenType(str, Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTokenManager:
    @classmethod
    def create(cls, data: dict, token_type: TokenType, duration: timedelta = timedelta(minutes=30)) -> str:
        now = datetime.now(timezone.utc)
        exp_time = now + duration
        payload = {**data, "exp": int(exp_time.timestamp()), "type": token_type.value}
        assert config.JWT_ALGORITHM, "JWT algorithm not found"
        return jwt.encode(payload, config.JWT_SINGING_KEY, algorithm=config.JWT_ALGORITHM)

    @staticmethod
    def verify(token: str, expected_type: Optional[str] = None) -> JWTPayload | None:
        assert config.JWT_ALGORITHM, "JWT algorithm not found"

        try:
            options, algorithms = {"verify_sub": False}, [config.JWT_ALGORITHM]
            payload = jwt.decode(token, config.JWT_SINGING_KEY, algorithms, options)
        except ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Expired token")
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

        if expected_type and payload.get("type") != expected_type:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token type mismatch")
        return JWTPayload(**payload)


class PasswordManager:
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
