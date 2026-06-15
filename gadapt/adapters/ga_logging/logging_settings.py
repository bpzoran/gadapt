import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

from gadapt.utils.TimeStampFormatter import TimestampFormatter

# Maximum log file size in bytes (default: 5 MB)
MAX_LOG_FILE_SIZE = 20 * 1024 * 1024
# Number of backup log files to keep
BACKUP_COUNT = 5


def init_logging(is_logging: bool):
    """
    Initializes logging for genetic algorithm
    """
    logger = logging.getLogger("gadapt_logger")
    if not is_logging:
        logger.disabled = True
        return
    else:
        logger.disabled = False
    path = os.path.join(os.getcwd(), "log")
    if not os.path.exists(path):
        os.mkdir(path)
    now = datetime.datetime.now()

    formatted_date_time = (
        now.strftime("%Y_%m_%d_%H_%M_%S_") + f"{now.microsecond // 1000:03d}"
    )
    logpath = os.path.join(path, f"gadapt_log_{formatted_date_time}.log")
    handler = RotatingFileHandler(
        logpath,
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=BACKUP_COUNT
    )
    handler.setFormatter(
        TimestampFormatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def gadapt_log_info(msg: str):
    logger = logging.getLogger("gadapt_logger")
    if logger.disabled:
        return
    try:
        logger.info(msg)
    except Exception:
        pass


def gadapt_log_warning(msg: str):
    logger = logging.getLogger("gadapt_logger")
    if logger.disabled:
        return
    try:
        logger.warning(msg)
    except Exception:
        pass


def gadapt_log_error(msg: str):
    logger = logging.getLogger("gadapt_logger")
    try:
        logger.error(msg)
    except Exception:
        pass
