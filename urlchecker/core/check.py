"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import csv
import os
import random
import re
import sys
from typing import Dict, List

from urlchecker.core import fileproc
from urlchecker.core.urlproc import UrlCheckResult
from urlchecker.core.worker import Workers


class UrlChecker:
    """
    The UrlChecker can be instantiated by a client, and then used
    to parse files, extract urls, and save results.
    """

    def __init__(
        self,
        path: str = None,
        file_types: List[str] = None,
        exclude_files: List[str] = None,
        print_all: bool = True,
        include_patterns: List[str] = None,
        serial: bool = False,
    ):
        """
        initiate a url checker. At init we take in preferences for
        file extensions, excluding preferences, and other initial
        parameters to run a url check.

        Args:
            - path              (str) : full path to the root folder to check. If not defined, no file_paths are parsed.
            - file_types       (list) : types of files to scan for links.
            - print_all        (bool) : control var for whether to print all checked file names or only the ones with urls.
            - exclude_files    (list) : list of excluded files and patterns for flies.
            - include_patterns (list) : list of files and patterns to check.
            - serial           (bool) : do checks in serial (no multiprocessing)
        """
        # Initiate results object, and checks lookup (holds UrlCheck) for each file
        self.results = {
            "passed": set(),
            "failed": set(),
            "excluded": set(),
        }  # type: Dict[str, set]

        # Results organized by filename
        self.checks = {}  # type: Dict[str, Dict]

        # Save run parameters
        self.exclude_files = exclude_files or []
        self.include_patterns = include_patterns or []
        self.print_all = print_all
        self.path = path
        self.file_types = file_types or [".py", ".md"]
        self.file_paths = []
        self.serial = serial

        # get all file paths if a path is defined
        if path:

            # Exit early if path not defined
            if not os.path.exists(path):
                sys.exit("%s does not exist." % path)

            self.file_paths = fileproc.get_file_paths(
                base_path=path,
                file_types=self.file_types,
                exclude_files=self.exclude_files,
                include_patterns=self.include_patterns,
            )

    def __str__(self) -> str:
        if self.path:
            return "UrlChecker:%s" % self.path
        return "UrlChecker"

    def __repr__(self) -> str:
        return self.__str__()

    def save_results(
        self,
        file_path: str,
        sep: str = ",",
        header: List[str] = None,
        relative_paths: bool = True,
    ) -> str:
        """
        Given a check_results dictionary, a dict with "failed" and "passed" keys (
        or more generally, keys to indicate some status), save a csv
        file that has header with URL,RESULT that indicates, for each url,
        a pass or failure. If the directory of the file path doesn't exist, exit
        on error.

        Args:
            - file_path       (str) : the file path (.csv) to save to.
            - sep             (str) : the separate to use (defaults to comma)
            - header         (list) : if not provided, will save URL,RESULT
            - relative_paths (bool) : save relative paths (default True)

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
                        file_name = re.sub(self.path, "", file_name).strip("/")
                    else:
                        file_name = os.path.relpath(file_name)

                [
                    writer.writerow([url, "failed", file_name])
                    for url in result["failed"]
                ]
                [
                    writer.writerow([url, "excluded", file_name])
                    for url in result["excluded"]
                ]
                [
                    writer.writerow([url, "passed", file_name])
                    for url in result["passed"]
                ]

        return file_path

    def run(
        self,
        file_paths: List[str] = None,
        exclude_patterns: List[str] = None,
        exclude_urls: List[str] = None,
        retry_count: int = 2,
        timeout: int = 5,
    ) -> Dict[str, set]:
        """
        Run the url checker given a path, excluded patterns for urls/files
        name paths or patterns, and a number of retries and timeouts.
        This provides a wrapper to check_files, which expects an already
        determined listing of files.

        Args:
            - file_paths       (list) : list of file paths to run over, defaults to those generated on init.
            - exclude_urls     (list) : list of excluded urls.
            - exclude_patterns (list) : list of excluded patterns for urls.
            - retry_count       (int) : number of retries on failed first check. Default=2.
            - timeout           (int) : timeout to use when waiting on check feedback. Default=5.

        Returns:
            dictionary with each of list of urls for "failed" and "passed."
        """
        file_paths = file_paths or self.file_paths

        # Allow for user to skip specifying excluded options
        exclude_urls = exclude_urls or []
        exclude_patterns = exclude_patterns or []

        # Run with multiprocessing
        tasks = {}
        funcs = {}
        workers = Workers()

        # Each run should have its own port (~2k)
        ports = list(range(8000, 9999))
        random.shuffle(ports)

        # loop through files
        results = {}
        for file_name in file_paths:

            # Re-use ports if we run out
            if not ports:
                ports = list(range(8000, 9999))

            # Export parameters and functions, use the same check task for all
            kwargs = {
                "file_name": file_name,
                "exclude_patterns": exclude_patterns,
                "exclude_urls": exclude_urls,
                "print_all": self.print_all,
                "retry_count": retry_count,
                "timeout": timeout,
                "port": ports.pop(0),
            }

            if self.serial:
                results[file_name] = check_task(**kwargs)
                continue

            tasks[file_name] = kwargs
            funcs[file_name] = check_task

        if not self.serial:
            results = workers.run(funcs, tasks)  # type: ignore
        if not results:
            print("\U0001F914 There were no URLs to check.")
            return self.results

        for file_name, result in results.items():
            self.checks[file_name] = result
            self.results["failed"].update(result["failed"])
            self.results["passed"].update(result["passed"])
            self.results["excluded"].update(result["excluded"])

        # A flattened dict of passed and failed
        return self.results


def check_task(*args, **kwargs):
    """
    A checking task, the default we use
    """
    # Instantiate a checker to extract urls
    checker = UrlCheckResult(
        file_name=kwargs["file_name"],
        exclude_patterns=kwargs.get("exclude_patterns", []),
        exclude_urls=kwargs.get("exclude_urls", []),
        print_all=kwargs.get("print_all", True),
    )

    # Check the urls
    checker.check_urls(
        retry_count=kwargs.get("retry_count", 2),
        timeout=kwargs.get("timeout", 5),
        port=kwargs.get("port"),
    )

    # Update flattened results
    return {
        "failed": checker.failed,
        "passed": checker.passed,
        "excluded": checker.excluded,
    }
