import pytest
from db import Database
from dotenv import dotenv_values
from models.device import Device

secrets = dotenv_values(".env")
TEST_DB_URL = secrets.get("test_db_url")


class TestDevicesTable:
    @pytest.fixture(scope="class")
    def db(self):   
        print("this ran")
        db = Database(TEST_DB_URL)
        db.delete_device_table()
        db.create_tables()
        return db
    
    @pytest.fixture(autouse=True, scope="class")
    def close_connection(self, db):
        yield
        db.close_connection()
        

    @pytest.fixture(autouse=True, scope="class")
    def seed_fake_data(self, db):   

        seeds = [
            Device(name="Christmas Tree", color_mode="rgb", ip_address="192.168.1.211"),
            Device(name="Book Shelf", color_mode="rgb", ip_address="192.168.1.14"),
            Device(name="items", color_mode="rgb", ip_address="192.168.1.7"),
            Device(name="test items", color_mode="rgb", ip_address="192.168.1.6"),
            Device(name="kitchen", color_mode="rgb", ip_address="192.168.1.101"),
            Device(name="Bathroom", color_mode="rgb", ip_address="192.168.1.47"),
            Device(name="Dining Table", color_mode="rgb", ip_address="192.168.1.87")
        ]

        for seed in seeds :
            db.session.add(seed)

        db.commit()

    def test_has_correct_item_count(self, db):
        EXPECTED_COUNT_BEFORE = 7
        devices = [device for device in db.get_all_devices()]
        assert len(devices) == EXPECTED_COUNT_BEFORE


    def test_can_create_device(self, db):
        EXPECTED_COUNT = 8

        db.session.add(Device(name="NEW Item", color_mode="rgb", ip_address="192.168.1.65"))
        db.commit()

        devices = [device for device in db.get_all_devices()]
        assert len(devices) == EXPECTED_COUNT

