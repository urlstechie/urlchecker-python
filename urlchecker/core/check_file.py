"""

Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import csv
import os
import re
import sys
from urlchecker.core.check import UrlChecker


class UrlCheckerFile(UrlChecker):
    """The UrlCheckerFile can be instantiated by a client, and then used
    to parse files, extract urls, and save results.
    """

    def __init__(
        self,
        files=None,
        print_all=True,
    ):
        """
        initiate a url checker. At init we take in preferences for
        file extensions, excluding preferences, and other initial
        parameters to run a url check.

        Args:
            - files            (list) : list of files to check.
            - print_all        (str) : control var for whether to print all checked file names or only the ones with urls.
        """
        # Initiate results object, and checks lookup (holds UrlCheck) for each file
        self.results = {"passed": set(), "failed": set(), "excluded": set()}
        self.checks = {}

        # Save run parameters
        self.print_all = print_all
        self.file_paths = []

        # Check that all files specified exist and are not directories
        if files:
            for file in files:
                # Exit early if path not defined
                if not os.path.exists(file):
                    sys.exit("%s does not exist." % file)
                # Exit early if a directory was provided
                if os.path.isdir(file):
                    sys.exit("%s is a directory. only files are accepted in this mode." % file)

        self.file_paths = files

    def __str__(self):
        if self.path:
            return "UrlCheckerFile:%s" % self.path
        return "UrlCheckerFile"
