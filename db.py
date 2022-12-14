
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

    def create_tables(self):
        device.create_table(self.engine)

    def delete_all_tables(self):
        device.Device.__table__.drop(self.engine)

    def commit(self):
        self.session.commit()

    def get_all_devices(self):
        return self.session.query(device.Device)

    def close_connection(self):
        self.session.close()
