"""

Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

__version__ = "0.0.25"
AUTHOR = "Ayoub Malek, Vanessa Sochat"
AUTHOR_EMAIL = "superkogito@gmail.com, vsochat@stanford.edu"
NAME = "urlchecker"
PACKAGE_URL = "http://www.github.com/urlstechie/urlchecker-python"
KEYWORDS = "urls, static checking, checking, validation"
DESCRIPTION = (
    "tool to collect and validate urls over static files (code and documentation)"
)
LICENSE = "LICENSE"


################################################################################
# Global requirements


INSTALL_REQUIRES = (("requests", {"min_version": "2.18.4"}),)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
