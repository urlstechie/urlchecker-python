#!/usr/bin/python

"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""


import os
import sys
import argparse
import urlchecker
import logging

def get_parser():
    parser = argparse.ArgumentParser(description="urlchecker python")

    # Global Variables
    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        help="urlchecker python actions",
        title="actions",
        description='actions for urlchecker',
        dest="command",
    )

    # print version and exit
    subparsers.add_parser(
        "version", help="show software version"  # pylint: disable=unused-variable
    )

    # main check entrypoint
    check = subparsers.add_parser(
        "check", help="check urls in static files (documentation or code)"
    )

    # supports a clone URL or a path
    check.add_argument(
        "path",
        help="the local path or GitHub repository to clone and check",
    )

    check.add_argument(
        "-b",
        "--branch",
        help="if cloning, specify a branch to use (defaults to master)",
        default="master",
    )

    check.add_argument(
        "--subfolder",
        help="relative subfolder path within path (if not specified, we use root)",
    )

    check.add_argument(
        "--cleanup",
        help="remove root folder after checking (defaults to False, no cleaup)",
        default=False,
        action="store_true",
    )

    check.add_argument(
        "--force-pass",
        help="force successful pass (return code 0) regardless of result",
        default=False,
        action="store_true",
    )

    check.add_argument(
        "--no-print",
        help="Skip printing results to the screen (defaults to printing to console).",
        default=False,
        action="store_true",
    )

    check.add_argument(
        "--file-types",
        dest="file_types",
        help="comma separated list of file extensions to check (defaults to .md,.py)",
        default=".md,.py",
    )

# White listing

    check.add_argument(
        "--white-listed-urls",
        help="comma separated list of white listed urls (no spaces)",
        default="",
    )

    check.add_argument(
        "--white-listed-patterns",
        help="comma separated list of white listed patterns for urls (no spaces)",
        default="",
    )

    check.add_argument(
        "--white-listed-files",
        help="comma separated list of white listed files and patterns for files (no spaces)",
        default="",
    )

# Saving

    check.add_argument(
        "--save",
        help="Path toa csv file to save results to.",
        default=None,
    )

# Timeouts

    check.add_argument(
        "--retry-count",
        help="retry count upon failure (defaults to 2, one retry).",
        type=int,
        default=2,
    )

    check.add_argument(
        "--timeout",
        help="timeout (seconds) to provide to the requests library (defaults to 5)",
        type=int,
        default=5,
    )

    return parser


def main():
    """main is the entrypoint urlchecker-python.
    """

    parser = get_parser()

    def help(return_code=0):
        """print help, including the software version and active client 
           and exit with return code.
        """

        version = urlchecker.__version__

        print("\nurlchecker python v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Show the version and exit
    if args.command == "version" or args.version:
        print(urlchecker.__version__)
        sys.exit(0)

    if args.command == "check":
        from .check import main
    else:
        print("Unsupported command %s" % args.command)
        sys.exit(0)
    
    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, extra=extra)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
