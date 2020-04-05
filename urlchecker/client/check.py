"""
client/github.py: entrypoint for interaction with a GitHub repostiory.
Copyright (c) 2020 Ayoub Malek and Vanessa Sochat
"""

import re
import os
import sys
import logging

from urlchecker.main.github import clone_repo, delete_repo
from urlchecker.core.fileproc import remove_empty, save_results
from urlchecker.core.check import run_urlchecker
from urlchecker.logger import print_success, print_failure

logger = logging.getLogger('urlchecker')


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

    # Parse file types, and white listed urls and files (includes absolute and patterns)
    file_types = args.file_types.split(",")
    white_listed_urls = remove_empty(args.white_listed_urls.split(","))
    white_listed_patterns = remove_empty(args.white_listed_patterns.split(","))
    white_listed_files = remove_empty(args.white_listed_files.split(","))

    # Alert user about settings
    print("  original path: %s" % args.path)
    print("     final path: %s" % path)
    print("      subfolder: %s" % args.subfolder)
    print("         branch: %s" % args.branch)
    print("        cleanup: %s" % args.cleanup)
    print("     file types: %s" % file_types)
    print("      print all: %s" % (not args.no_print))
    print(" url whitetlist: %s" % white_listed_urls)
    print("   url patterns: %s" % white_listed_patterns)
    print("  file patterns: %s" % white_listed_files)
    print("     force pass: %s" % args.force_pass)
    print("    retry count: %s" % args.retry_count)
    print("           save: %s" % args.save)
    print("        timeout: %s" % args.timeout)

    # Run checks, get lookup of results and fails
    check_results = run_urlchecker(path=path,
                                   file_types=file_types,
                                   white_listed_files=white_listed_files,
                                   white_listed_urls=white_listed_urls,
                                   white_listed_patterns=white_listed_patterns,
                                   print_all=not args.no_print,
                                   retry_count=args.retry_count,
                                   timeout=args.timeout)

    # save results to flie, if save indicated
    if args.save:
        save_results(check_results, args.save)

    # delete repo when done, if requested
    if args.cleanup:
        logger.info("Cleaning up %s..." % path)
        delete_repo(path)

    # Case 1: We didn't find any urls to check
    if not check_results['failed'] and not check_results['passed']:
        print("\n\nDone. No urls were collected.")
        sys.exit(0)

    # Case 2: We had errors, but force pass is True
    elif args.force_pass and check_results['failed']:
        print("\n\nDone. The following urls did not pass:")
        for failed_url in check_results['failed']:
            print_failure(failed_url)
        sys.exit(1)

    else:
        print("\n\nDone. All URLS passed.")
        sys.exit(0)
