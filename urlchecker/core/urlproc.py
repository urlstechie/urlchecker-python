"""

Copyright (c) 2020-2021 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import sys
import time
import random
import asyncio
import aiohttp
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
    if response.status == 200:
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


class UrlCheckResult:
    """A UrlCheckResult is a basic class to hold a result for a filename.
    It includes passed, failed, and all urls for a particular file,
    along with taking the filename and parsing it for urls.
    """

    def __init__(
        self,
        file_name=None,
        exclude_patterns=None,
        exclude_urls=None,
        print_all=True,
    ):
        self.file_name = file_name
        self.print_all = print_all
        self.passed = []
        self.failed = []
        self.excluded = []
        self.urls = []
        self.exclude_patterns = exclude_patterns or []
        self.exclude_urls = exclude_urls or []
        self.extract_urls()

    def __str__(self):
        if self.file_name:
            return "UrlCheckResult:%s" % self.file_name
        return "UrlCheckResult"

    def __repr__(self):
        return self.__str__()

    @property
    def all(self):
        """All returns all urls found in a file name, including those that
        passed and failed.
        """
        return self.passed + self.failed + self.excluded

    @property
    def count(self):
        return len(self.all)

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
        self.urls = fileproc.collect_links_from_file(self.file_name)

    async def aysnc_url_check(self, url, retry_count, timeout, headers):
        """
        Asyncronous check function for one url.

        Args:
            - urls           (list) : a list of urls to check.
            - retry_count    (int)  : a number of retries to issue (defaults to 1, no retry).
            - timeout        (int)  : a timeout in minutes for blocking operations like the connection attempt.
            - headers        (dict) : headers to use in the request.
        """
        # init do retrails and retrails counts
        do_retry = True
        rcount = retry_count

        # we will double the time for retry each time
        retry_seconds = 15

        # With retry, increase timeout by a second
        pause = timeout
        saved_responses = []
        saved_errors = []

        try:
            while rcount > 0 and do_retry:
                response = None
                async with aiohttp.ClientSession(headers=headers) as session:
                    try:
                        async with session.get(
                            url=url,
                            raise_for_status=False,
                            timeout=aiohttp.ClientTimeout(pause * 60),
                        ) as url_response:
                            response = url_response

                        # if success! Retry is not needed.
                        if response is not None:
                            do_retry = False if (response.status == 200) else True
                            if (response.status == 200) and (rcount == retry_count):
                                print_success(url)
                            else:
                                saved_responses.append(response)

                    except Exception as e:
                        saved_errors.append(e)
                        response = None

                # decrement retrials count
                rcount -= 1

                # If we try again, pause for retry seconds and update retry seconds
                if rcount > 0 and do_retry:
                    # keep this only for debugging
                    await asyncio.sleep(retry_seconds)
                    retry_seconds = retry_seconds * 2
                    pause += 1

            if len(saved_errors) > 0 or len(saved_responses) > 0:
                print_failure(url)
                # print errors
                for error_msg in saved_errors:
                    print("\x1b[33m" + "> " + str(error_msg) + "\x1b[0m")

                # print pevious url checks responses
                for response_msg in saved_responses[1:]:
                    check_response_status_code(url, response_msg)

            # When we break from while, we record final response
            self.record_response(url, response)

        except Exception as e:
            print(e)

    async def async_urls_check(self, urls, retry_count, timeout, headers):
        """
        Wrapper function for the asyncronous urls check.

        Args:
            - urls           (list) : a list of urls to check.
            - retry_count    (int)  : a number of retries to issue (defaults to 1, no retry).
            - timeout        (int)  : a timeout in minutes for blocking operations like the connection attempt.
            - headers        (dict) : headers to use in the request.
        """
        ret = await asyncio.gather(
            *[self.aysnc_url_check(url, retry_count, timeout, headers) for url in urls]
        )

    def check_urls(self, urls=None, retry_count=3, timeout=5):
        """
        Check urls extracted from a certain file and print the checks results.

        Args:
            - urls           (list) : a list of urls to check.
            - retry_count    (int)  : a number of retries to issue (defaults to 1, no retry).
            - timeout        (int)  : a timeout in minutes for blocking operations like the connection attempt.
        """
        urls = urls or self.urls

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
                if self.file_name:
                    print("\n", self.file_name, "\n", "-" * len(self.file_name))
                print("No urls found.")
            return

        if self.file_name:
            print("\n", self.file_name, "\n", "-" * len(self.file_name))

        # init seen urls list
        seen = set()

        # Some sites will return 403 if it's not a "human" user agent
        user_agent = get_user_agent()
        headers = {"User-Agent": user_agent}

        # check urls asyncronously
        unique_urls = set([url for url in urls if "http" in url])

        # handle different py versions support
        if (3, 7) <= sys.version_info:
            asyncio.run(
                self.async_urls_check(unique_urls, retry_count, timeout, headers)
            )
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                asyncio.wait(
                    [
                        self.aysnc_url_check(url, retry_count, timeout, headers)
                        for url in unique_urls
                    ]
                )
            )

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
        elif response.status == 200:
            self.passed.append(url)

        # Any other error
        else:
            self.failed.append(url)
