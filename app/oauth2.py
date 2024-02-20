from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import get_db
from app.redis_part import redis_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_with_scope(required_scopes: List[str] = None):
    def dependency(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Check if the token is blacklisted
            if redis_client.exists(f"blacklist:{token}"):
                raise HTTPException(status_code=401, detail="Token has been revoked")

            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_exception

            # Retrieve the session token stored in Redis
            stored_token = redis_client.get(f"user_session:{user_id}")
            # Verify the provided token matches the stored token
            if not stored_token or stored_token != token:
                raise HTTPException(status_code=401, detail="Session has been invalidated")

            # Check if the required scopes are present in the token's scopes
            user_scopes: List[str] = payload.get("scopes", [])
            if required_scopes and not set(required_scopes).issubset(set(user_scopes)):
                raise HTTPException(status_code=403, detail="Insufficient permissions")

            # Fetch the user from the database
            user = db.query(models.User).filter(models.User.id == user_id).first()
            if user is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        return user

    return dependency
