# ------------------------- Libraries -------------------------
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db
from app.oauth2 import get_current_user_with_scope
from app.validator import bod_validator, validate_password
from app.redis_part import add_emails_to_whitelist

# ------------------------- Implement Users with SQLALCHEMY -------------------------
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(get_current_user_with_scope(required_scopes=["read:items"]))):
    # noinspection PyTypeChecker
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        user_id = 0
    else:
        user_id = user.id
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not allowed to perform requested action")

    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validate_password(password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Password is too weak.")
    # hash the password - user.password
    hashed_password = utils.hash_pass(user.password)
    user.password = hashed_password
    bod_validator(bod=user.DoB)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # with open("WHITELISTED_EMAILS.txt", "w") as f:
    #     f.write(f"{new_user.email}\n")
    add_emails_to_whitelist(new_user.email)
    return new_user


@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(get_current_user_with_scope(required_scopes=["update:items"]))):
    # noinspection PyTypeChecker
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        user_id = 0
    else:
        user_id = user.id
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not allowed to perform requested action")

    bod_validator(bod=updated_user.DoB)
    hashed_password = utils.hash_pass(updated_user.password)
    updated_user.password = hashed_password
    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user
