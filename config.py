from pathlib import Path
from dotenv import dotenv_values
from simple_logging import get_basic_logger


secrets = dotenv_values(".env")

TEST_DB_URL = "sqlite+pysqlite:///.test_db.db"
DB_CONNECT_STR = "sqlite+pysqlite:///.rgb_everywhere.db"

# Creates a logging object to use
log = get_basic_logger()
