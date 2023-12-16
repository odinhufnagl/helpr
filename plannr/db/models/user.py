from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .util import Base, id_column, created_at_column, updated_at_column
import bcrypt
from logger import logger


@dataclass
class DBUser(Base):
    __tablename__ = "user"
    id: Mapped[int] = id_column()
    created_at: Mapped[datetime] = created_at_column()
    updated_at: Mapped[datetime] = updated_at_column()
    email: Mapped[str] = mapped_column(String, unique=True) #TODO: add email validation #TODO: email should be primary-key right?, or at least not two users with same email
    _password_hash = mapped_column(String)

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password: str):
        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        self._password_hash = pwhash.decode('utf-8')
    
    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash.encode('utf-8')) 