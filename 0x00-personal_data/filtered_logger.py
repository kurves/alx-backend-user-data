#!/usr/bin/env python3
"""
Module that provides a function to obfuscate log messages.
"""

from typing import List
import re

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in the log message.
    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda x: f"{x.group().split('=')[0]}={redaction}", message)
