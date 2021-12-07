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
from urlchecker.core.check import UrlChecker
from urlchecker.logger import print_failure

logger = logging.getLogger("urlchecker")


def main(args, extra):
    """
    main entrypoint for running a check. We expect an args object with
    arguments from the main client. From here we determine the path
    to parse (or GitHub url to clone) and call the main check function
    under main/check.py

    Parameters:
      - args: the argparse ArgParser with parsed args
      - extra: extra arguments not handled by the parser
    """
    path = args.path

    # Case 1: specify present working directory
    if not path or path == ".":
        path = os.getcwd()
        logging.debug("Path specified as present working directory, %s" % path)

    # Case 2: We need to clone
    elif re.search("^(git@|http)", path):
        logging.debug("Repository url %s detected, attempting clone" % path)
        path = clone_repo(path, branch=args.branch)

    # Add subfolder to path
    if args.subfolder:
        path = os.path.join(path, args.subfolder)

    # By the time we get here, a path must exist
    if not os.path.exists(path):
        sys.exit("Error %s does not exist." % path)

    # Parse file types, and excluded urls and files (includes absolute and patterns)
    file_types = args.file_types.split(",")
    exclude_urls = remove_empty(args.exclude_urls.split(","))
    exclude_patterns = remove_empty(args.exclude_patterns.split(","))
    exclude_files = remove_empty(args.exclude_files.split(","))
    files = remove_empty(args.files.split(","))

    # Alert user about settings
    print("           original path: %s" % args.path)
    print("              final path: %s" % path)
    print("               subfolder: %s" % args.subfolder)
    print("                  branch: %s" % args.branch)
    print("                 cleanup: %s" % args.cleanup)
    print("              file types: %s" % file_types)
    print("                   files: %s" % files)
    print("               print all: %s" % (not args.no_print))
    print("                 verbose: %s" % (args.verbose))
    print("           urls excluded: %s" % exclude_urls)
    print("   url patterns excluded: %s" % exclude_patterns)
    print("  file patterns excluded: %s" % exclude_files)
    print("              force pass: %s" % args.force_pass)
    print("             retry count: %s" % args.retry_count)
    print("                    save: %s" % args.save)
    print("                 timeout: %s" % args.timeout)

    # Instantiate a new checker with provided arguments
    checker = UrlChecker(
        path=path,
        file_types=file_types,
        include_patterns=files,
        exclude_files=exclude_files,
        print_all=not args.no_print,
    )
    check_results = checker.run(
        exclude_urls=exclude_urls,
        exclude_patterns=exclude_patterns,
        retry_count=args.retry_count,
        timeout=args.timeout,
    )

    # save results to file, if save indicated
    if args.save:
        checker.save_results(args.save)

    # delete repo when done, if requested
    if args.cleanup:
        logger.info("Cleaning up %s..." % path)
        delete_repo(path)

    # Case 1: We didn't find any urls to check
    if not check_results["failed"] and not check_results["passed"]:
        print("\n\n\U0001F937. No urls were collected.")
        sys.exit(0)

    # Case 2: We had errors, print them for the user
    if check_results["failed"]:
        if args.verbose:
            print("\n\U0001F914 Uh oh... The following urls did not pass:")
            for file_name, result in checker.checks.items():
                print_failure(file_name + ":")
                for url in result.failed:
                    print_failure("     " + url)
        else:
            print("\n\U0001F914 Uh oh... The following urls did not pass:")
            for failed_url in check_results["failed"]:
                print_failure(failed_url)

    # If we have failures and it's not a force pass, exit with 1
    if not args.force_pass and check_results["failed"]:
        sys.exit(1)

    # Finally, alert user if we are passing conditionally
    if check_results["failed"]:
        print("\n\U0001F928 Conditional pass force pass True.")
    else:
        print("\n\n\U0001F389 All URLS passed!")
    sys.exit(0)
