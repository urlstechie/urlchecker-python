"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import csv
import os
import re
import sys
from urlchecker.core import fileproc
from urlchecker.core.urlproc import UrlCheckResult


class UrlChecker:
    """The UrlChecker can be instantiated by a client, and then used
       to parse files, extract urls, and save results.
    """

    def __init__(
        self,
        path=None,
        file_types=None,
        white_listed_files=None,
        print_all=True,
        include_patterns=None,
    ):
        """
        initiate a url checker. At init we take in preferences for
        file extensions, white listing preferences, and other initial
        parameters to run a url check.

        Args:
            - path                   (str) : full path to the root folder to check. If not defined, no file_paths are parsed
            - print_all              (str) : control var for whether to print all checked file names or only the ones with urls.
            - white_listed_files    (list) : list of white-listed files and patterns for flies.
            - include_patterns      (list) : list of files and patterns to check.
        """
        # Initiate results object, and checks lookup (holds UrlCheck) for each file
        self.results = {"passed": set(), "failed": set(), "white_listed": set()}
        self.checks = {}

        # Save run parameters
        self.white_listed_files = white_listed_files or []
        self.include_patterns = include_patterns or []
        self.print_all = print_all
        self.path = path
        self.file_types = file_types or [".py", ".md"]
        self.file_paths = []

        # get all file paths if a path is defined
        if path:

            # Exit early if path not defined
            if not os.path.exists(path):
                sys.exit("%s does not exist." % path)

            self.file_paths = fileproc.get_file_paths(
                include_patterns=self.include_patterns,
                base_path=path,
                file_types=self.file_types,
                white_listed_files=self.white_listed_files,
            )

    def __str__(self):
        if self.path:
            return "UrlChecker:%s" % self.path
        return "UrlChecker"

    def __repr__(self):
        return self.__str__()

    def save_results(self, file_path, sep=",", header=None, relative_paths=True):
        """
        Given a check_results dictionary, a dict with "failed" and "passed" keys (
        or more generally, keys to indicate some status), save a csv
        file that has header with URL,RESULT that indicates, for each url,
        a pass or failure. If the directory of the file path doesn't exist, exit
        on error.

        Args:
            - file_path (str): the file path (.csv) to save to.
            - sep (str): the separate to use (defaults to comma)
            - header (list): if not provided, will save URL,RESULT
            - relative paths (bool) : save relative paths (default True)

        Returns:
            (str) file_path: a newly saved csv with the results
        """
        # Ensure that the directory exists
        file_path = os.path.abspath(file_path)
        dirname = os.path.dirname(file_path)

        if not os.path.exists(dirname):
            sys.exit("%s does not exist, cannot save %s there." % (dirname, file_path))

        # Ensure the header is provided and correct (length 2)
        if not header:
            header = ["URL", "RESULT", "FILENAME"]

        if len(header) != 3:
            sys.exit("Header must be length 3 to match size of data.")

        print("Saving results to %s" % file_path)

        # Write to file after header row
        with open(file_path, mode="w") as fd:
            writer = csv.writer(
                fd, delimiter=sep, quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(header)

            # Iterate through filenames, each with check results
            for file_name, result in self.checks.items():

                # Derive the relative path based on self.path, or relative to run
                if relative_paths:
                    if self.path:
                        file_name = re.sub(self.path, "", file_name).strip('/')
                    else:
                        file_name = os.path.relpath(file_name)

                [writer.writerow([url, "failed", file_name]) for url in result.failed]
                [writer.writerow([url, "white_listed", file_name]) for url in result.white_listed]
                [writer.writerow([url, "passed", file_name]) for url in result.passed]

        return file_path

    def run(
        self,
        file_paths=None,
        white_listed_patterns=None,
        white_listed_urls=None,
        retry_count=2,
        timeout=5,
    ):
        """
        Run the url checker given a path, a whitelist for each of url and file
        name paths or patterns, and a number of retries and timeouts.
        This provides a wrapper to check_files, which expects an already
        determined listing of files.

        Args:
            - file_paths            (list) : list of file paths to run over, defaults to those generated on init.
            - white_listed_urls     (list) : list of white-listed urls.
            - white_listed_patterns (list) : list of white-listed patterns for urls.
            - retry_count            (int) : number of retries on failed first check. Default=2.
            - timeout                (int) : timeout to use when waiting on check feedback. Default=5.

        Returns: dictionary with each of list of urls for "failed" and "passed."
        """
        file_paths = file_paths or self.file_paths

        # Allow for user to skip specifying white listed options
        white_listed_urls = white_listed_urls or []
        white_listed_patterns = white_listed_patterns or []

        # loop through files files
        for file_name in file_paths:

            # Instantiate a checker to extract urls
            checker = UrlCheckResult(
                file_name=file_name,
                white_listed_patterns=white_listed_patterns,
                white_listed_urls=white_listed_urls,
                print_all=self.print_all,
            )

            # Check the urls
            checker.check_urls(retry_count=retry_count, timeout=timeout)

            # Update flattened results
            self.results["failed"].update(checker.failed)
            self.results["passed"].update(checker.passed)
            self.results["white_listed"].update(checker.white_listed)

            # Save the checker in the lookup
            self.checks[file_name] = checker

        # A flattened dict of passed and failed
        return self.results
