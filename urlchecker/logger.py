"""

Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import logging


def print_failure(message):
    """
    Given a message string, print as a failure in red.

    Parameters:
      - message: the message to print in red (indicating failure).
    """
    print("\x1b[31m" + message + "\x1b[0m")


def print_success(message):
    """
    Given a message string, print as a success in green.

    Parameters:
      - message: the message to print in green (indicating success).
    """
    print("\x1b[32m" + message + "\x1b[0m")


def get_logger(name="urlchecker", level=logging.INFO):
    """
    Get a default logger for the urlchecker library, meaning
    that we use name "urlchecker" and use the default logging
    level INFO

    Parameters:
      - name: the name for the logger (defaults to urlchecker)
      - level: the logging.<level> to set with setLevel()

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
