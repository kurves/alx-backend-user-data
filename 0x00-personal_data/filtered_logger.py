#!/usr/bin/env python3
"""
Module that provides a function to obfuscate log messages.
"""

from typing import List
import re
import logging

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in the log message.
    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda x: f"{x.group().split('=')[0]}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter instance.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, applying field redaction.
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for PII.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
