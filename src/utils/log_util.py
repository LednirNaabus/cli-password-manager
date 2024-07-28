import logging

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Sets up a logger for file and console handlers.

    Args:
        name (str, required): The name of the logger.
        log_file (str, required): The name of the log file.
    """

    base_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(base_format)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(base_format)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
