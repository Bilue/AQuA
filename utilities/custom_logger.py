import os
import logging
import sys
from logging.handlers import RotatingFileHandler

"""


This code creates a logging mechanism for an application. It creates several handlers for 
different log levels (ERROR, WARNING, DEBUG, and INFO), sets each handler's level and formatter, and adds each 
handler to a logger object. The handlers write log messages to different log files and also to the console. 
Additionally, the script uses a rotating file handler to limit the size of the log file. The logs are organized in 
several directories (Error, Warning, Debug, and Info) inside a Logs directory. The logger object is returned so it 
can be used in other parts of the application.

@author Gaurav Purwar

"""
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class LogGen:
    @staticmethod
    def loggen():
        # Create a handler for each log level
        error_handler = logging.FileHandler(os.path.join("logs/error", "error.log"))
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        warning_handler = logging.FileHandler(os.path.join("logs/warning", "warning.log"))
        warning_handler.setLevel(logging.WARNING)
        warning_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        debug_handler = logging.FileHandler(os.path.join("logs/debug", "debug.log"))
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Create a handler for the console output
        info_handler = logging.StreamHandler(sys.stdout)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Create a rotating file handler for the HTML report output
        file_handler = RotatingFileHandler('logs/info/logs.log', maxBytes=100000, backupCount=10)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Add the handlers to the logger
        logger.addHandler(error_handler)
        logger.addHandler(warning_handler)
        logger.addHandler(debug_handler)
        # logger.addHandler(info_handler)
        logger.addHandler(file_handler)

        return logger
