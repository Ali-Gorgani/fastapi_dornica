from datetime import timedelta, datetime, timezone

from fastapi import status, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import schemas, models, utils, oauth2
from app.database import get_db
from app.redis_part import check_whitelist_with_redis, redis_client, rate_limit

router = APIRouter(
    tags=['Authentication']
)


@router.post('/token', response_model=schemas.Token)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # rate limit
    client_ip = request.client.host + ":" + str(request.client.port)
    rate_limit(client_ip, limit=5, period=60)  # Allow 5 requests per minute per IP

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not check_whitelist_with_redis(user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_scopes = utils.get_user_scopes(user.role)

    # create a token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "scopes": user_scopes})
    print(f"{user.userName} has successfully logged in!")
    redis_client.set(f"user_session:{user.id}", access_token, ex=3600)  # Expires in 1 hour
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2.oauth2_scheme)):
    # Example token expiration, adjust according to your token management logic
    token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    ttl = int((token_expiration - datetime.now(timezone.utc)).total_seconds())

    # Ensure TTL is positive
    if ttl > 0:
        redis_client.setex(f"blacklist:{token}", ttl, "true")
    else:
        # Handle error: token already expired or TTL calculation issue
        print("Error setting TTL for token.")
