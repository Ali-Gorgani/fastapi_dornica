from sqlalchemy import Column, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, Enum, Integer

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    userName = Column(String, nullable=False, unique=True)
    fullName = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    DoB = Column(String)
    gender = Column(Enum('MALE', 'FEMALE', 'NOT_SPECIFIED', name='gender_enum', create_type=True),
                    server_default='NOT_SPECIFIED')
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
    role = Column(Enum('ADMIN', 'USER', name='role_enum', create_type=True), server_default='USER')


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum("HOUSE", "APARTMENT", name='type_enum', create_type=True), nullable=False)
    availableNow = Column(Boolean, server_default="True")
    ownerId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
    owner = relationship("User")


class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
