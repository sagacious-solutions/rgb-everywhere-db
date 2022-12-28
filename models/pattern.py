from sqlalchemy import Column, Integer, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)


def create_table(engine):
    Base.metadata.create_all(engine)
