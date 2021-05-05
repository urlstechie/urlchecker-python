"""
client/github.py: entrypoint for interaction with a GitHub repostiory.
Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat
"""

import re
import os
import sys
import logging

from urlchecker.main.github import clone_repo, delete_repo
from urlchecker.core.fileproc import remove_empty
from urlchecker.core.check_file import UrlCheckerFile
from urlchecker.logger import print_failure

logger = logging.getLogger("urlchecker")


def main(args, extra):
    """
    alternate entrypoint for running a check on specific files.
    We expect an args object with arguments from the main client.
    From here we check the arguments and call the main check function
    under main/check.py

    Parameters:
      - args: the argparse ArgParser with parsed args
      - extra: extra arguments not handled by the parser
    """

    # For the check_ci command path is always the current working directory (.)
    path = os.getcwd()

    # By the time we get here, a path must exist
    if not os.path.exists(path):
        sys.exit("Error %s does not exist." % path)

    # Parse file types, and excluded urls and files (includes absolute and patterns)
    file_types = ['*']
    exclude_urls = remove_empty(args.exclude_urls.split(","))

    files = args.files

    # Alert user about settings
    print("              final path: %s" % path)
    print("              file types: %s" % file_types)
    print("                   files: %s" % files)
    print("               print all: %s" % (not args.no_print))
    print("           urls excluded: %s" % exclude_urls)
    print("              force pass: %s" % args.force_pass)
    print("             retry count: %s" % args.retry_count)
    print("                    save: %s" % args.save)
    print("                 timeout: %s" % args.timeout)

    # Instantiate a new checker with provided arguments
    checker = UrlCheckerFile(
        files=files
    )
    check_results = checker.run(
        exclude_urls=exclude_urls,
        retry_count=args.retry_count,
        timeout=args.timeout,
    )

    # save results to flie, if save indicated
    if args.save:
        checker.save_results(args.save)

    # Case 1: We didn't find any urls to check
    if not check_results["failed"] and not check_results["passed"]:
        print("\n\nDone. No urls were collected.")
        sys.exit(0)

    # Case 2: We had errors, print them for the user
    if check_results["failed"]:
        print("\n\nDone. The following urls did not pass:")
        for failed_url in check_results["failed"]:
            print_failure(failed_url)

    # If we have failures and it's not a force pass, exit with 1
    if not args.force_pass and check_results["failed"]:
        sys.exit(1)

    # Finally, alert user if we are passing conditionally
    if check_results["failed"]:
        print("\n\nConditional pass force pass True.")
    else:
        print("\n\nDone. All URLS passed.")
    sys.exit(0)
