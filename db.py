
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models.device as device
from dotenv import dotenv_values
from sqlalchemy.orm import declarative_base

Base = declarative_base()
secrets = dotenv_values(".env")


class Database:
    def __init__(self, url):
        self.engine = create_engine(url, echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.create_tables()

    def add_device(self, new_device: Dict[str, str]):
        new_db_entry = device.Device(**new_device)
        self.session.add(new_db_entry)
        self.session.commit()

    def create_tables(self):
        device.create_table(self.engine)

    def delete_device_table(self):
        device.Device.__table__.drop(self.engine)

    def get_all_devices(self):
        return self.session.query(device.Device)

    def close_connection(self):
        self.session.close()
