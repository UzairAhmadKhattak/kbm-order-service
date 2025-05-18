# logger_config.py
import logging

def setup_logger(name: str) -> logging.Logger:
    """Returns a configured logger for the given module name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  # Prevent duplicate handlers
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger
