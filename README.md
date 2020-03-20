[![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/urlstechie/urlchecker-python/blob/master/LICENSE)

# urlchecker python

This is a python module to collect urls over static files (code and documentation)
and then test for and report broken links.

## Code documentation

A detailed documentation of the code is available under [urls-checker.readthedocs.io](https://urls-checker.readthedocs.io/en/latest/)

## Development

### Organization

The module is organized as follows:

```
├── client              # command line client
├── main                # functions for supported integrations (e.g., GitHub)
├── core                # core file and url processing tools
└── version.py          # package and versioning
```

In the "client" folder, for example, the commands that are exposed for the client 
(e.g., check) would named accordingly, e.g., `client/check.py`.
Functions for Github are be provided in `main/github.py`. This organization should
be fairly straight forward to always find what you are looking for.
