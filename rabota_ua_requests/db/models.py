from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    ARRAY,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Job(Base):
    __tablename__ = 'job'
    url = Column(
        String,
        primary_key=True,
    )
    city = Column(
        String,
    )
    title = Column(
        String,
        nullable=False,
    )
    contact_person = Column(
        String,
    )
    contact_numbers = Column(
        ARRAY(
            String,
        ),
    )
    created_at = Column(
        DateTime,
        default=func.now(),
    )
