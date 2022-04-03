"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

from typing import List


def excluded(
    url: str, exclude_urls: List[str] = None, exclude_patterns: List[str] = None
) -> bool:
    """
    Check if link is in the excluded URLs or patterns to ignore.

    Args:
        - url               (str) : link to check.
        - exclude_urls     (list) : list of excluded urls.
        - exclude_patterns (list) : list of excluded patterns.

    Returns:
        (bool) boolean for whether link is excluded or not.
    """
    exclude_urls = exclude_urls or []
    exclude_patterns = exclude_patterns or []

    # check excluded urls
    if url in exclude_urls:
        return True

    # check excluded patterns
    for exclude_pattern in exclude_patterns:
        if exclude_pattern in url:
            return True

    # default return
    return False
