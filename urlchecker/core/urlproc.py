"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import random
import time
from typing import Any, Dict, List, Optional

import requests
from fake_useragent import UserAgent

from urlchecker.core import fileproc
from urlchecker.core.exclude import excluded
from urlchecker.logger import print_failure, print_success


def check_response_status_code(
    url: str, response: Optional[requests.models.Response]
) -> bool:
    """
    Check response status of an input url. Returns a boolean
    to indicate if retry is needed.

    Args:
        - url                    (str) : url text.
        - response (requests.Response) : request response from the url request.

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


def get_user_agent() -> dict:
    """
    Return a randomly chosen user agent and headers for requests

    Returns:
        headers dict to include with request.
    """
    browser = random.choice(["chrome", "firefox"])
    headers = get_faux_headers(browser)
    headers["User-Agent"] = getattr(UserAgent(), browser)
    return headers


def get_faux_headers(browser) -> Dict[Any, Any]:
    """
    Get faux headers to populate based on user agent
    """
    headers = {
        "chrome": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        },
        "firefox": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        },
    }
    return headers[browser]


class UrlCheckResult:
    """
    A UrlCheckResult is a basic class to hold a result for a filename.
    It includes passed, failed, and all urls for a particular file, along with
    taking the filename and parsing it for urls.
    """

    def __init__(
        self,
        file_name: str = None,
        exclude_patterns: List[str] = None,
        exclude_urls: List[str] = None,
        print_all: bool = True,
    ):
        self.file_name = file_name
        self.print_all = print_all
        self.passed = []  # type: List[str]
        self.failed = []  # type: List[str]
        self.excluded = []  # type: List[str]
        self.urls = []  # type: List[str]
        self.exclude_patterns = exclude_patterns or []
        self.exclude_urls = exclude_urls or []

        # Only extract if we have a filename in advance
        if self.file_name:
            self.extract_urls()

    def __str__(self) -> str:
        if self.file_name:
            return "UrlCheckResult:%s" % self.file_name
        return "UrlCheckResult"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def all(self) -> List[str]:
        """
        All returns all urls found in a file name, including those that
        passed and failed.
        """
        return self.passed + self.failed + self.excluded

    @property
    def count(self) -> int:
        return len(self.all)

    def get_driver(self, port: Optional[int] = None, timeout: Optional[int] = 5):
        """
        Get a selenium web driver for a check session, if possible.
        Requires selenium driver to exit, fall back to not using
        """
        try:
            from .webdriver import WebDriver

            return WebDriver(port=port, timeout=timeout)
        except:
            return

    def extract_urls(self):
        """
        Typically on init, use the provided exclude patterns and urls to
        extract a list of urls for the given filename.
        """
        if not self.file_name or not os.path.exists(self.file_name):
            print(
                "File name %s is undefined or does not exist, skipping extraction."
                % self.file_name
            )
            return

        # collect all links from file (unique=True is set)
        self.urls = fileproc.collect_links_from_file(self.file_name)

    def check_urls(
        self,
        urls: List[str] = None,
        retry_count: int = 1,
        timeout: int = 5,
        port: Optional[int] = None,
    ) -> None:
        """
        Check urls extracted from a certain file and print the checks results.

        Args:
            - urls          (list) : list of urls.
            - retry_count    (int) : a number of retries to issue (defaults to 1, no retry).
            - timeout        (int) : a timeout in seconds for blocking operations like the connection attempt.
            - port           (int) : a port for the driver to use (if installed)
        """
        urls = urls or self.urls

        # Set driver (session) at start of check
        driver = self.get_driver(port, timeout)

        # eliminate excluded urls and patterns
        if self.exclude_urls or self.exclude_patterns:
            self.excluded = [
                url
                for url in urls
                if excluded(url, self.exclude_urls, self.exclude_patterns)
            ]
            urls = list(set(urls).difference(set(self.excluded)))

        # if no urls are found, mention it if required
        if not urls:
            if self.print_all:
                print("No urls found.")
            return

        # init seen urls list
        seen = set()

        # check links
        for url in [url for url in urls if "http" in url]:

            # Some sites will return 403 if it's not a "human" user agent
            headers = get_user_agent()

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

                    # Fallback to trying selenium driver for any error code
                    if (
                        response.status_code not in [200, 404]
                        and driver
                        and driver.check(url)
                    ):
                        response.status_code = 200

                # Web driver doesn't have same issues with ssl
                except Exception as e:
                    if driver and driver.check(url):
                        response = requests.Response()
                        response.status_code = 200
                    else:
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

        # Close driver at end of session
        if driver:
            driver.close()

    def record_response(self, url: str, response: Optional[requests.models.Response]):
        """
        Record response status of an input url. This function is run after success,
        or at the end of retry to record the final response.

        Args:
            - url                    (str) : url text.
            - response (requests.Response) : request response from the url request.
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
