# logger.py

import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to set up a logger with timed rotating file handler.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (logging.Level): Logging level, default is logging.INFO.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Check if the logs directory exists, if not, create it
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a timed rotating file handler
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
    handler.setLevel(level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger

# Usage example
# logger = setup_logger('performance_monitor', 'logs/performance_monitor.log')
