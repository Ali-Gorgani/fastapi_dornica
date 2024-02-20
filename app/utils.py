from typing import List

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str):
    return pwd_context.hash(password)


def verify_pass(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --------------------- User access scopes ---------------------

ROLE_TO_SCOPES = {
    "USER": ["read:items", "create:items", "delete:items", "update:items"],
    "ADMIN": ["read:items", "create:items", "delete:items", "update:items"],
}


def get_user_scopes(user_role: str) -> List[str]:
    """Retrieve a list of scopes based on the user's role."""
    return ROLE_TO_SCOPES.get(user_role, [])
