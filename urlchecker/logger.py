"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import logging


def print_failure(message: str):
    """
    Given a message string, print as a failure in red.

    Args:
      - message (str): the message to print in red (indicating failure).
    """
    print("\033[91m" + message + "\033[0m")


def print_success(message: str):
    """
    Given a message string, print as a success in green.

    Args:
      - message (str): the message to print in green (indicating success).
    """
    print("\033[92m" + message + "\033[0m")


def get_logger(name: str = "urlchecker", level: int = logging.INFO) -> logging.Logger:
    """
    Get a default logger for the urlchecker library, meaning
    that we use name "urlchecker" and use the default logging
    level INFO

    Parameters:
      - name  (str) : the name for the logger (defaults to urlchecker)
      - level (int) : the logging.<level> to set with setLevel()

    Returns: logging logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # formatting
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
