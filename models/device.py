from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

import json

Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    color_mode = Column(String(3))
    ip_address = Column(String)

    def __repr__(self):
        return (f'id: {self.id} name: {self.name} color_mode: {self.color_mode} ip_address: {self.ip_address}')

    def get_dict(self):
        temp_dict = {}

        for key, item in self.__dict__.items():
            if key.startswith('_'):
                continue
            temp_dict[key] = item

        return temp_dict


def create_table(engine):
    Base.metadata.create_all(engine)


christmas_tree = Device(name="Christmas Tree", color_mode="rgb", ip_address="192.168.1.211")