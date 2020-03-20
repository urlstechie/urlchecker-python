"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

def white_listed(url, white_listed_urls, white_listed_patterns):
    """
    Check if link is in the white listed URLs or patterns to ignore.

    Args:
        - url                    (str) : link to check.
        - white_listed_urls     (list) : list of white-listed urls.
        - white_listed_patterns (list) : list of white-listed patterns.

    Returns:
        (bool) boolean for whether link is white-listed or not.
    """
    # check white listed urls
    if url in white_listed_urls:
        return True

    # check white listed patterns
    i = 0
    while i < len(white_listed_patterns):
        if white_listed_patterns[i] in url:
            return True
        i += 1

    # default return
    return False
