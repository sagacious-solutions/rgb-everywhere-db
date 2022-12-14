from pathlib import Path
from dotenv import dotenv_values
from simple_logging import get_basic_logger


secrets = dotenv_values(".env")

# Creates a logging object to use
log = get_basic_logger()
