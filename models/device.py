from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    color_mode = Column(String(3))
    ip_address = Column(String)



def create_table(engine):
    Base.metadata.create_all(engine)

christmas_tree = Device(name="Christmas Tree", color_mode="rgb", ip_address="192.168.1.211")