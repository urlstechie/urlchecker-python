# CHANGELOG

This is a manually generated log to track changes to the repository for each release.
Each section should include general headers such as **Implemented enhancements**
and **Merged pull requests**. Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults or behavior
 - backward incompatible changes

Referenced versions in headers are tagged on Github, in parentheses are for pypi.

## [vxx](https://github.com/urlstechie/urlschecker-python/tree/master) (master)
 - preparing to install from git for fake-useragent (0.0.33)
 - serial option for debugging (0.0.32)
 - adding support for web driver for harder URLs (0.0.31)
 - use ANSI escape sequences for colors, fake-useragent for agents (0.0.30)
 - adding type hints to code, more tests and logging bug fix (0.0.29)
 - decrease verbosity when filename is None (0.0.28)
 - don't exit and fail if no URLs to check (0.0.27)
 - multiprocessing to speed up checks (0.0.26)
 - bug fix for verbose option to only print file names that have failures (0.0.25)
 - adding option to print a summary that contains file names and urls (0.0.24)
 - updating container base to use debian buster and adding certifi (0.0.23)
 - updating "whitelist" arguments to exclude (0.0.22)
 - adding support for dotfiles for a file type (0.0.21)
 - final regexp needs to again parse away { or } (0.0.20)
 - csv save uses relative paths (0.0.19)
 - adding white_listed to print of results
 - urls that end in {expression} are filtered out
 - refactor check.py to be UrlChecker class, save with filename (0.0.18)
 - default for files needs to be empty string (not None) (0.0.17)
 - bug with incorrect return code on fail, add files flag (0.0.16)
 - reverting back to working client (0.0.15)
 - removing unused file variable (0.0.13)
 - adding support for csv export (0.0.12)
 - fixing bug with parameter type for retry count and timeout (0.0.11)
 - first release of urlchecker module with container, tests, and brief documentation (0.0.1)
 - dummy release for pypi (0.0.0)
