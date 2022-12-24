import pytest
from db import Database
from dotenv import dotenv_values
from models.device import Device
import config

secrets = dotenv_values(".env")
# TEST_DB_URL = secrets.get("test_db_url")
TEST_DB_URL = config.TEST_DB_URL


class TestDevicesTable:
    @pytest.fixture(scope="class")
    def db(self):
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
            Device(
                name="Christmas Tree",
                color_order="rgb",
                ip_address="192.168.1.211",
                pixel_count=100,
            ),
            Device(
                name="Book Shelf",
                color_order="rgb",
                ip_address="192.168.1.14",
                pixel_count=100,
            ),
            Device(
                name="items",
                color_order="rgb",
                ip_address="192.168.1.7",
                pixel_count=100,
            ),
            Device(
                name="test items",
                color_order="rgb",
                ip_address="192.168.1.6",
                pixel_count=100,
            ),
            Device(
                name="kitchen",
                color_order="rgb",
                ip_address="192.168.1.101",
                pixel_count=100,
            ),
            Device(
                name="Bathroom",
                color_order="rgb",
                ip_address="192.168.1.47",
                pixel_count=100,
            ),
            Device(
                name="Dining Table",
                color_order="rgb",
                ip_address="192.168.1.87",
                pixel_count=100,
            ),
        ]

        for seed in seeds:
            db.session.add(seed)

        db.session.commit()

    def test_has_correct_item_count(self, db):
        EXPECTED_COUNT_BEFORE = 7
        devices = [device for device in db.get_all_devices()]
        assert len(devices) == EXPECTED_COUNT_BEFORE

    def test_can_create_device(self, db):
        EXPECTED_COUNT = 8
        db.add_device(
            {
                "name": "NEW Item",
                "color_order": "rgb",
                "ip_address": "192.168.1.65",
            }
        )
        devices = [device for device in db.get_all_devices()]
        assert len(devices) == EXPECTED_COUNT

    def test_can_get_specific_device(self, db):
        ACTUAL_DEVICE = db.get_device("192.168.1.87")
        EXPECTED_DEVICE_NAME = "Dining Table"
        assert ACTUAL_DEVICE.name == EXPECTED_DEVICE_NAME

    def test_can_update_device(self, db):
        EXPECTED_DEVICE_NAME = "Updated Item"
        db.update_device({"ip_address": "192.168.1.87", "name": "Updated Item"})

        UPDATED_DEVICE = db.get_device("192.168.1.87")

        assert UPDATED_DEVICE.name == EXPECTED_DEVICE_NAME

    def test_can_delete_device(self, db):
        EXPECTED_COUNT = 7
        db.delete_device({"ip_address": "192.168.1.65"})
        devices = [device for device in db.get_all_devices()]
        assert len(devices) == EXPECTED_COUNT
