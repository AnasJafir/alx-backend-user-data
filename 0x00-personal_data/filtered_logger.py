#!/usr/bin/env python3
"""Obfuscating Module"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated
    Args:
        fields (list): List of field names to obfuscate.
        redaction (str): String to replace field values with.
        message (str): The original log message.
        separator (str): The character separating fields in the message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
                rf'{field}=.+?{separator}',
                f'{field}={redaction}{separator}',
                message
                )
    return message
