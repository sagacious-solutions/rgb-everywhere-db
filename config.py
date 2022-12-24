from pathlib import Path
from dotenv import dotenv_values
from simple_logging import get_basic_logger


secrets = dotenv_values(".env")

TEST_DB_PATH = Path.cwd() / ".test_db.db"
DB_PATH = Path.cwd() / ".rgb_everywhere.db"

TEST_DB_CONNECT_STR = f"sqlite+pysqlite:///{TEST_DB_PATH.as_posix()}"
DB_CONNECT_STR = f"sqlite+pysqlite:///{DB_PATH.as_posix()}"

# Creates a logging object to use
log = get_basic_logger()
