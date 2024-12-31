import logging
import coloredlogs

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    coloredlogs.install(
        logger=logger,
        level='INFO',
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
