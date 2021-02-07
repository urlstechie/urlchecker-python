"""

Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import fnmatch
import re
import os
from urlchecker.core import urlmarker


def check_file_type(file_path, file_types):
    """
    Check file type to assert that only file with certain predefined extensions
    are checked. We currently support an extension verbatim, or regular
    expression to match the filename. For example, .* matches all hidden files,
    and *.html matches an html file.

    Args:
        - file_path   (str) : path to file.
        - file_types (list) : list of file extensions to accept.

    Returns:
        (bool) true if file type is supported else false.
    """
    ftype = "." + file_path.split(".")[-1]
    if ftype in file_types:
        return True

    # The user can also provide a regular expression
    if any(fnmatch.fnmatch(file_path, x) for x in file_types):
        return True

    # default return
    return False


def include_file(file_path, exclude_patterns=None, include_patterns=None):
    """
    Check a file path for inclusion based on an OR regular expression.
    The user is currently not notified if a file is marked for removal.

    Args:
        - file_path        (str) : a file path to check if should be included.
        - exclude_patterns (list) : list of patterns to exclude.
        - include_patterns (list) : list of patterns to include.

    Returns:
        (bool) boolean indicating if the URL should be excluded (not tested).
    """
    include_patterns = include_patterns or []
    exclude_patterns = exclude_patterns or []

    # No excluded patterns, all files are included
    if not exclude_patterns and not include_patterns:
        return True

    # Create a regular expression for each
    exclude_regexp = "(%s)" % "|".join(exclude_patterns)
    include_regexp = "(%s)" % "|".join(include_patterns)

    # Return False (don't include) if excluded
    if not include_patterns:
        return not re.search(exclude_regexp, file_path)

    # We have an include_patterns only
    elif not exclude_patterns:
        return re.search(include_regexp, file_path)

    # If both defined, excluded takes preference
    return re.search(include_regexp, file_path) and not re.search(
        exclude_regexp, file_path
    )


def get_file_paths(base_path, file_types, exclude_files=None, include_patterns=None):
    """
    Get path to all files under a give directory and its subfolders.

    Args:
        - base_path           (str) : base path.
        - file_types         (list) : list of file extensions to accept.
        - include_patterns   (list) : list of files and patterns to include.
        - exclude_files (list) : list of files or patterns to exclude

    Returns:
        (list) list of file paths.
    """
    exclude_files = exclude_files or []
    include_patterns = include_patterns or []

    # init paths
    file_paths = []

    # walk folders and colect file paths
    for root, directory, files in os.walk(base_path):
        file_paths += [
            os.path.join(root, file)
            for file in files
            if os.path.isfile(os.path.join(root, file))
            and check_file_type(file, file_types)
            and include_file(os.path.join(root, file), exclude_files, include_patterns)
        ]
    return file_paths


def collect_links_from_file(file_path, unique=True):
    """
    Collect all links in a file.

    Args:
        - file_path   (str) : path to file.

    Returns:
        (list) list of links/ urls in a file.
    """
    # read file content
    with open(file_path, "r") as file:
        content = file.read()

    # get and filter urls
    urls = re.findall(urlmarker.URL_REGEX, content)
    urls = [url.strip() for url in urls if url.strip().startswith("http")]
    urls = [url.strip("\\n") if url.endswith("\\n") else url for url in urls]

    # filter urls including {}
    urls = [url for url in urls if not re.search("(\\{[a-z0-9.]*})", url)]

    # Final cleaning of URLS
    final = []
    for url in urls:
        match = re.match(urlmarker.FINAL_REGEX, url)
        if match:
            final.append(url[match.start() : match.end()])

    # Do we only want unique links?
    if unique:
        return list(set(final))

    return final


def remove_empty(file_list):
    """
    Given a file list, return only those that aren't empty string or None.

    Args:
        - file_list (list): a list of files to remove None or empty string from.

    Returns:
        (list) list of (non None or empty string) contents.
    """
    return [x for x in file_list if x not in ["", None]]
