#!/usr/bin/env python3
"""Obfuscating Module"""
import re
from typing import List
import logging
from os import environ
import mysql.connector


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum
        """
        return filter_datum(
                self.fields,
                self.REDACTION,
                super().format(record),
                self.SEPARATOR
                )


def get_logger() -> logging.Logger:
    """
    Returns a logging object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(
            RedactingFormatter(
                list(("name", "email", "phone", "ssn", "password"))
                )
            )
    logger.addHandler(handler)
    return logger


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password',)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """function that returns a connector to the database"""
    db = mysql.connector.connection.MySQLConnection(
        host=environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=environ.get("PERSONAL_DATA_DB_NAME"),
        user=environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    )
    return db
