"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import time
import random
import requests
from urlchecker.core import fileproc
from urlchecker.core.exclude import excluded
from urlchecker.logger import print_success, print_failure


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


def find_urls(file_names, exclude_patterns=None, exclude_urls=None):
    """
    Given a list of file names, return the file name and a list of urls to parse
    (intended to be passed on to the UrlCheckResultResult class) that removes
    any redundant URLs.
    """
    # keep a master list of urls we have seen - no repeats allowed!
    seen = set()

    for file_name in file_names:
        checker = UrlCheckResult(
            file_name=file_name,
            exclude_patterns=exclude_patterns,
            exclude_urls=exclude_urls,
        )

        # Ensure we don't have repeats and updated seen list
        checker.urls = [u for u in checker.urls if u not in seen]
        [seen.add(u) for u in checker.urls]

        # Skip empty sets of urls
        if not checker.urls:
            continue

        # finder.urls is already unique
        yield file_name, checker.urls


class UrlCheckResult:
    """
    A UrlCheckResult is a basic class to find urls, check, and hold results.
    It includes passed, failed, and all urls for a particular file,
    along with taking the filename and parsing it for urls.
    """

    def __init__(
        self,
        file_name=None,
        print_all=True,
        exclude_patterns=None,
        exclude_urls=None,
        urls=None,
    ):
        self.file_name = file_name
        self.urls = urls or []
        self.print_all = print_all
        self.passed = []
        self.failed = []
        self.excluded = []
        self.exclude_patterns = exclude_patterns or []
        self.exclude_urls = exclude_urls or []

        # Only parse urls from file if not provided
        if not self.urls:
            self.extract_urls()

    def __str__(self):
        if self.file_name:
            return "UrlCheckResult:%s" % self.file_name
        return "UrlCheckResult"

    def __repr__(self):
        return self.__str__()

    def extract_urls(self):
        """Typically on init, use the provided exclude patterns and urls to
        extract a list of urls for the given filename.
        """
        if not self.file_name or not os.path.exists(self.file_name):
            print(
                "File name %s is undefined or does not exist, skipping extraction."
                % self.file_name
            )
            return

        # collect all links from file (unique=True is set)
        urls = fileproc.collect_links_from_file(self.file_name)

        # eliminate excluded urls and patterns
        if self.exclude_urls or self.exclude_patterns:
            self.excluded = [
                url
                for url in urls
                if excluded(url, self.exclude_urls, self.exclude_patterns)
            ]
            urls = list(set(urls).difference(set(self.excluded)))

        self.urls = urls

    @property
    def all(self):
        """All returns all urls found in a file name, including those that
        passed and failed.
        """
        return self.passed + self.failed + self.excluded

    @property
    def count(self):
        return len(self.all)

    def check_urls(self, urls=None, retry_count=1, timeout=5):
        """
        Check urls extracted from a certain file and print the checks results.

        Args:
            - retry_count    (int) : a number of retries to issue (defaults to 1, no retry).
            - timeout        (int) : a timeout in seconds for blocking operations like the connection attempt.
        """
        urls = urls or self.urls

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
            self.record_response(url, response)

    def record_response(self, url, response):
        """
        Record response status of an input url. This function is run after success,
        or at the end of retry to record the final response.

        Args:
            - url          (str) : url text.
            - response    (list) : request response from the url request.
        """
        # response of None indicates a failure
        if not response:
            self.failed.append(url)

        # success
        elif response.status_code == 200:
            self.passed.append(url)

        # Any other error
        else:
            self.failed.append(url)
