"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.1"
AUTHOR = "Ayoub Malek, Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
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
