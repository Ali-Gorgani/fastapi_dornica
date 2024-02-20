from faker import Faker

from app.database import SessionLocal
from app.models import User
from app.utils import hash_pass

fake = Faker()


def seed_users_with_hashed_passwords():
    db = SessionLocal()
    for _ in range(3):
        username = fake.user_name()
        email = fake.email()
        # Now using hashed passwords
        password = hash_pass(fake.password())
        user = User(userName=username, email=email, password=password)
        db.add(user)
        print(f"Added user: {username}")
    db.commit()
    db.close()
