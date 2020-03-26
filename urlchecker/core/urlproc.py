"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import time
import random
import requests
from urlchecker.core import urlmarker
from urlchecker.logger import print_success, print_failure

def record_response(url, response, check_results):
    """
    Record response status of an input url. This function is run after success,
    or at the end of retry to record the final response.

    Args:
        - url          (str) : url text.
        - response    (list) : request response from the url request.
        - check_results (list) : list of lists, success appended to 0, failure to 1.
    """
    # response of None indicates a failure
    if not response:
        check_results["failed"].append(url)

    # success
    elif response.status_code == 200:
        check_results["passed"].append(url)

    # Any other error
    else:
        check_results["failed"].append(url)


def check_response_status_code(url, response):
    """
    Check response status of an input url. Returns a boolean
    to indicate if retry is needed.

    Args:
        - url          (str) : url text.
        - response    (list) : request response from the url request.

    Returns:
        (bool) boolean to indicate if retry is needed (True) or not (False)
    """
    # Case 1: response is None indicating triggered error
    if not response:
        print_failure(url)
        return True

    # Case 2: success! Retry is not needed.
    if response.status_code == 200:
        print_success(url)
        return False

    # Case 3: failure of some kind
    print_failure(url)
    return True


def get_user_agent():
    """
    Return a randomly chosen user agent for requests

    Returns:
        user agent string to include with User-Agent.
    """
    agents = [
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/57.0.2987.110 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/61.0.3163.79 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) "
            "Gecko/20100101 "
            "Firefox/55.0"
        ),  # firefox
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/61.0.3163.91 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/62.0.3202.89 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/63.0.3239.108 "
            "Safari/537.36"
        ),  # chrome
    ]
    return random.choice(agents)


def check_urls(urls, check_results, retry_count=1, timeout=5):
    """
    Check urls extracted from a certain file and print the checks results.

    Args:
        - urls          (list) : list of urls to check.
        - check_results (list) : a list containing a list of succesfully checked links and errenous links.
        - retry_count    (int) : a number of retries to issue (defaults to 1, no retry).
        - timeout        (int) : a timeout in seconds for blocking operations like the connection attempt.
    """
    # init seen urls list
    seen = set()

    # Some sites will return 403 if it's not a "human" user agent
    user_agent = get_user_agent()
    headers = {"User-Agent": user_agent}

    # check links
    for url in [url for url in urls if "http" in url]:

        # init do retrails and retrails counts
        do_retry = True
        rcount = retry_count

        # we will double the time for retry each time
        retry_seconds = 2

        # With retry, increase timeout by a second
        pause = timeout

        # get url termination
        url_termination = "." + os.path.basename(url).split(".")[-1]

        # No need to test the same URL twice
        if url in seen:
            continue

        seen.add(url)
        while rcount > 0 and do_retry:
            response = None
            try:
                response = requests.get(url, timeout=pause, headers=headers)

            except requests.exceptions.Timeout as e:
                print(e)

            except requests.exceptions.ConnectionError as e:
                print(e)

            except Exception as e:
                print(e)

            # decrement retrials count
            rcount -= 1

            # Break from the loop if we have success, update user
            do_retry = check_response_status_code(url, response)

            # If we try again, pause for retry seconds and update retry seconds
            if rcount > 0 and do_retry:
                # keep this only for debugging
                # print("Retry n° %s for %s, with timeout of %s seconds." % (retry_count - rcount, url, pause))
                time.sleep(retry_seconds)
                retry_seconds = retry_seconds * 2
                pause += 1

        # When we break from while, we record final response
        record_response(url, response, check_results)
