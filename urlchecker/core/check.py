"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import sys
from urlchecker.core import fileproc, urlproc
from urlchecker.core.whitelist import white_listed

def run_urlchecker(
    path,
    file_types,
    white_listed_files,
    white_listed_urls,
    white_listed_patterns,
    print_all,
    retry_count=2,
    timeout=5
):
    """
    Run the url checker given a path, a whitelist for each of url and file
    name paths or patterns, and a number of retries and timeouts.
    This provides a wrapper to check_files, which expects an already
    determined listing of files.

    Args:
        - path                   (str) : full path to the root folder to check.
        - print_all              (str) : control var for whether to print all checked file names or only the ones with urls.
        - white_listed_urls     (list) : list of white-listed urls.
        - white_listed_patterns (list) : list of white-listed patterns for urls.
        - white_listed_files    (list) : list of white-listed files and patterns for flies.
        - retry_count            (int) : number of retries on failed first check. Default=2.
        - timeout                (int) : timeout to use when waiting on check feedback. Default=5.

    Returns: dictionary with each of list of urls for "failed" and "passed."
    """
    if not os.path.exists(path):
        sys.exit("%s does not exist." % path)

    # get all file paths
    file_paths = fileproc.get_file_paths(
        base_path=path,
        file_types=file_types,
        white_listed_files=white_listed_files,
    )

    # check white listed list of files
    return check_files(
        file_paths=file_paths,
        print_all=print_all,
        white_listed_urls=white_listed_urls,
        white_listed_patterns=white_listed_patterns,
        retry_count=retry_count,
        timeout=timeout,
    )


def check_files(
    file_paths,
    print_all=True,
    white_listed_urls=None,
    white_listed_patterns=None,
    retry_count=2,
    timeout=5,
):
    """
    Check all urls extracted from all files in a given list.

    Args:
        - file_paths            (list) : list of file paths with urls to check (required).
        - print_all              (str) : control var for whether to print all checked file names or only the ones with urls.
        - white_listed_urls     (list) : list of white-listed urls.
        - white_listed_patterns (list) : list of white-listed url patterns.
        - retry_count            (int) : number of retries on failed first check. Default=1.
        - timeout                (int) : timeout to use when waiting on check feedback. Default=5.

    Returns:
        (list) check-results as a list of two lists (successfull checks, failed checks).
    """
    # init results list (first is success, second is issue)
    check_results = {"passed":[], "failed": []}

    # Allow for user to skip specifying white listed options
    white_listed_urls = white_listed_urls or []
    white_listed_patterns = white_listed_patterns or []

    # loop files
    for file_name in file_paths:

        # collect links from each file (unique=True is set)
        urls = fileproc.collect_links_from_file(file_name)

        # eliminate white listed urls and white listed white listed patterns
        if white_listed_urls:
            urls = [
                url
                for url in urls
                if not white_listed(url, white_listed_urls, white_listed_patterns)
            ]

        # if some links are found, check them
        if urls:
            print("\n", file_name, "\n", "-" * len(file_name))
            urlproc.check_urls(file_name, urls, check_results, retry_count, timeout)

        # if no urls are found, mention it if required
        else:
            if print_all:
                print("\n", file_name, "\n", "-" * len(file_name))
                print("No urls found.")

    return check_results
