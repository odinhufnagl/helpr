
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()

def id_column():
    return mapped_column(Integer(), primary_key=True)


def created_at_column():
    return mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def updated_at_column():
    return mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
