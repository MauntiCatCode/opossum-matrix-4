import logging
from pathlib import Path

FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"

MODULE_DIR = Path(__file__).resolve().parent
LOGFILE_PATH = MODULE_DIR.parent / "matrix.log"

logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        logging.FileHandler(LOGFILE_PATH, mode='a')]
)


log = logging.getLogger()

