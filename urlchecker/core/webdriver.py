"""

Copyright (c) 2022 Vanessa Sochat and Ayoub Malek

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

from selenium.common.exceptions import TimeoutException
from random import choice
from threading import Thread
from selenium import webdriver
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import re
import sys
import os

# Pattern when page doesn't exist
empty_page = "<html><head></head><body></body></html>"

# Install root (where we assume driver if not defined elsewhere)
root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class WebServer(SimpleHTTPRequestHandler):
    """
    Subclass SimpleHTTPServer to capture error messages
    """

    def log_message(self, format, *args):
        """
        Log to standard error with a date time string,
        """
        sys.stderr.write(
            "%s - - [%s] %s\n"
            % (self.address_string(), self.log_date_time_string(), format % args)
        )

        # Workaround for error trying to GET html
        if not re.search("div", format % args) and not re.search(
            "function", format % args
        ):
            if re.search("404", format % args):
                raise IOError(format % args)

    def log_error(self, format, *args):
        pass


class WebDriver:
    """
    Bring up a web server
    """

    def __init__(self, **kwargs):

        # Look for Chrome driver on path (will fail if not)
        self.set_driver()
        self.Handler = WebServer
        self.timeout = kwargs.get("timeout") or 10
        self.port = kwargs.get("port") or choice(range(8000, 9999))
        self.httpd = TCPServer(("", self.port), self.Handler)
        self.server = Thread(target=self.httpd.serve_forever)
        self.server.setDaemon(True)
        self.server.start()
        self.browser = None

    def set_driver(self, **kwargs):
        self.driver = kwargs.get("browser") or "Chrome"

        # The drivers must be on path (assume install root)
        path = os.environ.get("URLCHECKER_DRIVERS_PATH") or root
        new_path = "%s:%s" % (path, os.environ["PATH"])
        os.environ["PATH"] = new_path
        os.putenv("PATH", new_path)

    def check(self, url: str):
        """
        Check that a url is valid with the browser
        """
        self.get_browser()
        self.browser.implicitly_wait(3)
        self.browser.set_page_load_timeout(self.timeout)
        try:
            # This could technically be 404, but we are only calling for 403
            self.browser.get(url)
            return self.browser.title != "" and self.browser.page_source != empty_page
        except:
            return False
        return False

    def get_browser(self):
        """
        return a browser if it hasn't been initialized yet
        """
        if self.browser is None:
            if self.driver == "Firefox":
                self.browser = webdriver.Firefox()
            else:
                self.browser = webdriver.Chrome(chrome_options=self.get_options())
        return self.browser

    def get_options(self, width: int = 1200, height: int = 800):
        """
        Options for headless, no-sandbox, and custom width/height
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=%sx%s" % (width, height))
        return options

    def close(self):
        """
        Close any running browser or server, and shut down the robot
        """
        if self.browser is not None:
            self.browser.close()
        self.httpd.server_close()
