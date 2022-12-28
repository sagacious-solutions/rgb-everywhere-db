from typing import Dict, List
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import models.device as device
import models.pattern as pattern
from models.device import Device
from models.pattern import Pattern
from dotenv import dotenv_values
from sqlalchemy.orm import declarative_base

Base = declarative_base()
secrets = dotenv_values(".env")


class Database:
    def __init__(self, url):
        self.engine = create_engine(url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.create_tables()

    def add_device(self, new_device: Dict[str, str]):
        """Add a new Device to the database

        Args:
            new_device (Dict[str, str]): Device details to add to db
        """
        new_db_entry = device.Device(**new_device)
        self.session.add(new_db_entry)
        self.session.commit()

    def add_pattern(self, new_pattern: List[List[int]]):
        self.__check_pattern_valid(new_pattern)
        new_db_entry = pattern.Pattern(data={"pattern": new_pattern})
        self.session.add(new_db_entry)
        self.session.commit()

    def __check_pattern_valid(self, new_pattern: List[List[int]]):
        if not type(new_pattern) == list:
            raise ValueError(
                "Argument new_pattern must be a List of list of integers"
            )
        for value in new_pattern:
            if not type(value) == list or not len(value) == 3:
                raise ValueError(
                    "Argument new_pattern must be a List of lists of 3 integers"
                )

    def get_device(self, ip_address: str) -> Device:
        """Gets a specific device by IP address from the database

        Args:
            ip_address (str): IP Address of the new device

        Raises:
            ValueError: Thrown if we get multi results for an IP Address

        Returns:
            Device: The device you saught
        """

        devices = []
        query = select(Device.__table__).where(
            Device.__table__.c.ip_address == ip_address
        )
        for row in self.session.execute(query):
            devices.append(row)

        if len(devices) > 1:
            raise ValueError(
                "Database query should have returned only one result per IP"
                " Address."
            )

        return devices[0]

    def update_device(self, device_to_update: Dict[str, str]):
        """Updates an existing device in the database

        Args:
            device_to_update (Dict[str, str]): The device in the database to update

        Raises:
            ValueError: Raise if no device was provided to query database
        """
        if not device_to_update:
            raise ValueError("No device was passed to update function.")

        update_entry = (
            Device.__table__.update()
            .where(
                Device.__table__.c.ip_address
                == device_to_update.get("ip_address")
            )
            .values(**device_to_update)
        )
        self.session.execute(update_entry)
        self.session.commit()

    def delete_device(self, device_to_delete: Dict[str, str]):
        """Deletes a device from the provided dict from the database.

        It will use the ip_address key to locate the item

        Args:
            device_to_delete (Dict[str, str]): Device to delete, must have a ip_address
                key
        """
        delete_entry = Device.__table__.delete().where(
            Device.__table__.c.ip_address == device_to_delete.get("ip_address")
        )
        self.session.execute(delete_entry)
        self.session.commit()

    def create_tables(self):
        device.create_table(self.engine)
        pattern.create_table(self.engine)

    def delete_device_table(self):
        device.Device.__table__.drop(self.engine)

    def delete_pattern_table(self):
        pattern.Pattern.__table__.drop(self.engine)

    def get_all_devices(self):
        session = self.Session()
        return session.query(device.Device)

    def get_all_patterns(self):
        session = self.Session()
        return session.query(pattern.Pattern)

    def close_connection(self):
        self.session.close()
