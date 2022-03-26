<div style="text-align:center"><img src="https://raw.githubusercontent.com/urlstechie/urlchecker-python/master/docs/urlstechie.png"/></div>

[![Build Status](https://travis-ci.com/urlstechie/urlchecker-python.svg?branch=master)](https://travis-ci.com/urlstechie/urlchecker-python) [![Documentation Status](https://readthedocs.org/projects/urlchecker-python/badge/?version=latest)](https://urlchecker-python.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/urlstechie/urlchecker-python/branch/master/graph/badge.svg)](https://codecov.io/gh/urlstechie/urlchecker-python) [![Python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue)](https://www.python.org/doc/versions/) [![CodeFactor](https://www.codefactor.io/repository/github/urlstechie/urlchecker-python/badge)](https://www.codefactor.io/repository/github/urlstechie/urlchecker-python) ![PyPI](https://img.shields.io/pypi/v/urlchecker) [![Downloads](https://pepy.tech/badge/urlchecker)](https://pepy.tech/project/urlchecker) [![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/urlstechie/urlchecker-python/blob/master/LICENSE)


# urlchecker-python

This is a python module to collect urls over static files (code and documentation)
and then test for and report broken links. If you are interesting in using
this as a GitHub action, see [urlchecker-action](https://github.com/urlstechie/urlchecker-action). There are also container
bases available on [quay.io/urlstechie/urlchecker](https://quay.io/repository/urlstechie/urlchecker?tab=tags). As of version
0.0.26, we use multiprocessing so the checks run a lot faster, and you can set `URLCHECKER_WORKERS` to change the number of workers
(defaults to 9). If you don't want multiprocessing, use version 0.0.25 or earlier.

## Module Documentation

A detailed documentation of the code is available under [urlchecker-python.readthedocs.io](https://urlchecker-python.readthedocs.io/en/latest/)

## Usage

### Install

You can install the urlchecker from [pypi](https://pypi.org/project/urlchecker):

```bash
$ pip install urlchecker
```

or install from the repository directly:

```bash
$ git clone https://github.com/urlstechie/urlchecker-python.git
$ cd urlchecker-python
$ python setup.py install
```

Installation will place a binary, `urlchecker` in your Python path.

```bash
$ which urlchecker
/home/vanessa/anaconda3/bin/urlchecker
```


### Check Local Folder

Your most likely use case will be to check a local directory with static files (documentation or code)
for files. In this case, you can use urlchecker check:

```bash
$ urlchecker check --help
usage: urlchecker check [-h] [-b BRANCH] [--subfolder SUBFOLDER] [--cleanup]
                        [--force-pass] [--no-print] [--file-types FILE_TYPES]
                        [--files FILES] [--exclude-urls EXCLUDE_URLS]
                        [--exclude-patterns EXCLUDE_PATTERNS]
                        [--exclude-files EXCLUDE_FILES] [--save SAVE]
                        [--retry-count RETRY_COUNT] [--timeout TIMEOUT]
                        path

positional arguments:
  path                  the local path or GitHub repository to clone and check

optional arguments:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
                        if cloning, specify a branch to use (defaults to
                        master)
  --subfolder SUBFOLDER
                        relative subfolder path within path (if not specified,
                        we use root)
  --cleanup             remove root folder after checking (defaults to False,
                        no cleaup)
  --force-pass          force successful pass (return code 0) regardless of
                        result
  --no-print            Skip printing results to the screen (defaults to
                        printing to console).
  --file-types FILE_TYPES
                        comma separated list of file extensions to check
                        (defaults to .md,.py)
  --files FILES         comma separated list of exact files or patterns to
                        check.
  --exclude-urls EXCLUDE_URLS
                        comma separated links to exclude (no spaces)
  --exclude-patterns EXCLUDE_PATTERNS
                        comma separated list of patterns to exclude (no
                        spaces)
  --exclude-files EXCLUDE_FILES
                        comma separated list of files and patterns to exclude
                        (no spaces)
  --save SAVE           Path to a csv file to save results to.
  --retry-count RETRY_COUNT
                        retry count upon failure (defaults to 2, one retry).
  --timeout TIMEOUT     timeout (seconds) to provide to the requests library
                        (defaults to 5)
```

You have a lot of flexibility to define patterns of urls or files to skip,
along with the number of retries or timeout (seconds). The most basic usage will
check an entire directory. Let's clone and check the urlchecker action:

```bash
$ git clone https://github.com/urlstechie/urlchecker-action.git
$ cd urchecker-action
```

and run the simplest command to check the present working directory (.).

```bash
$ urlchecker check .
           original path: .
              final path: /tmp/urlchecker-action
               subfolder: None
                  branch: master
                 cleanup: False
              file types: ['.md', '.py']
                   files: []
               print all: True
           urls excluded: []
   url patterns excluded: []
  file patterns excluded: []
              force pass: False
             retry count: 2
                    save: None
                 timeout: 5

 /tmp/urlchecker-action/README.md 
 --------------------------------
https://github.com/urlstechie/urlchecker-action/blob/master/LICENSE
https://github.com/r-hub/docs/blob/bc1eac71206f7cb96ca00148dcf3b46c6d25ada4/.github/workflows/pr.yml
https://img.shields.io/static/v1?label=Marketplace&message=urlchecker-action&color=blue?style=flat&logo=github
https://github.com/rseng/awesome-rseng
https://github.com/rseng/awesome-rseng/blob/5f5cb78f8392cf10aec2f3952b305ae9611029c2/.github/workflows/urlchecker.yml
https://github.com/HPC-buildtest/buildtest-framework/actions?query=workflow%3A%22Check+URLs%22
https://www.codefactor.io/repository/github/urlstechie/urlchecker-action/badge
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks
https://github.com/urlstechie/urlchecker-action/issues
https://github.com/USRSE/usrse.github.io
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks/actions?query=workflow%3ACommands
https://github.com/USRSE/usrse.github.io/blob/abcbed5f5703e0d46edb9e8850eea8bb623e3c1c/.github/workflows/urlchecker.yml
https://github.com/urlstechie/urlchecker-action/releases
https://img.shields.io/badge/license-MIT-brightgreen
https://github.com/r-hub/docs/actions?query=workflow%3ACommands
https://github.com/rseng/awesome-rseng/actions?query=workflow%3AURLChecker
https://github.com/buildtesters/buildtest
https://github.com/r-hub/docs
https://www.codefactor.io/repository/github/urlstechie/urlchecker-action
https://github.com/urlstechie/URLs-checker-test-repo
https://github.com/marketplace/actions/urlchecker-action
https://github.com/actions/checkout
https://github.com/SuperKogito/URLs-checker/issues/1,https://github.com/SuperKogito/URLs-checker/issues/2
https://github.com/SuperKogito/URLs-checker/issues/1,https://github.com/SuperKogito/URLs-checker/issues/2
https://github.com/USRSE/usrse.github.io/actions?query=workflow%3A%22Check+URLs%22
https://github.com/SuperKogito/Voice-based-gender-recognition/issues
https://github.com/buildtesters/buildtest/blob/v0.9.1/.github/workflows/urlchecker.yml
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks/blob/master/.github/workflows/urlchecker-pr-label.yml

 /tmp/urlchecker-action/examples/README.md 
 -----------------------------------------
https://github.com/urlstechie/urlchecker-action/releases
https://github.com/urlstechie/urlchecker-action/issues
https://help.github.com/en/actions/reference/events-that-trigger-workflows


Done. The following urls did not pass:
https://github.com/SuperKogito/URLs-checker/issues/1,https://github.com/SuperKogito/URLs-checker/issues/2
```

The url that didn't pass above is an example parameter for the library! Let's add
a simple pattern to exclude it.

```bash
$ urlchecker check --exclude-pattern SuperKogito .
           original path: .
              final path: /tmp/urlchecker-action
               subfolder: None
                  branch: master
                 cleanup: False
              file types: ['.md', '.py']
                   files: []
               print all: True
           urls excluded: []
   url patterns excluded: ['SuperKogito']
  file patterns excluded: []
              force pass: False
             retry count: 2
                    save: None
                 timeout: 5

 /tmp/urlchecker-action/README.md 
 --------------------------------
https://github.com/urlstechie/urlchecker-action/blob/master/LICENSE
https://github.com/urlstechie/urlchecker-action/issues
https://github.com/rseng/awesome-rseng/actions?query=workflow%3AURLChecker
https://github.com/USRSE/usrse.github.io/actions?query=workflow%3A%22Check+URLs%22
https://github.com/actions/checkout
https://github.com/USRSE/usrse.github.io/blob/abcbed5f5703e0d46edb9e8850eea8bb623e3c1c/.github/workflows/urlchecker.yml
https://github.com/r-hub/docs/blob/bc1eac71206f7cb96ca00148dcf3b46c6d25ada4/.github/workflows/pr.yml
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks/blob/master/.github/workflows/urlchecker-pr-label.yml
https://github.com/rseng/awesome-rseng
https://www.codefactor.io/repository/github/urlstechie/urlchecker-action/badge
https://github.com/urlstechie/URLs-checker-test-repo
https://www.codefactor.io/repository/github/urlstechie/urlchecker-action
https://github.com/r-hub/docs
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks
https://github.com/buildtesters/buildtest
https://img.shields.io/badge/license-MIT-brightgreen
https://github.com/urlstechie/urlchecker-action/releases
https://github.com/marketplace/actions/urlchecker-action
https://img.shields.io/static/v1?label=Marketplace&message=urlchecker-action&color=blue?style=flat&logo=github
https://github.com/r-hub/docs/actions?query=workflow%3ACommands
https://github.com/HPC-buildtest/buildtest-framework/actions?query=workflow%3A%22Check+URLs%22
https://github.com/buildtesters/buildtest/blob/v0.9.1/.github/workflows/urlchecker.yml
https://github.com/berlin-hack-and-tell/berlinhackandtell.rocks/actions?query=workflow%3ACommands
https://github.com/USRSE/usrse.github.io
https://github.com/rseng/awesome-rseng/blob/5f5cb78f8392cf10aec2f3952b305ae9611029c2/.github/workflows/urlchecker.yml

 /tmp/urlchecker-action/examples/README.md 
 -----------------------------------------
https://help.github.com/en/actions/reference/events-that-trigger-workflows
https://github.com/urlstechie/urlchecker-action/issues
https://github.com/urlstechie/urlchecker-action/releases


Done. All URLS passed.
```

We can also filter by file types. If we want to do this (for example, to only check different file
types) we might do any of the following:

```bash
# Check only html files
urlchecker check --file-types *.html .

# Check hidden flies
urlchecker check --file-types ".*" .

# Check hidden files and html files
urlchecker check --file-types ".*,*.html" .
```

**Note that while some patterns will work without quotes, it's recommended for most**
to use them because if the shell expands any part of the pattern, it will not work as
expected. By default, the urlchecker checks python and markdown.

### Check GitHub Repository

But wouldn't it be easier to not have to clone the repository first?
Of course! We can specify a GitHub url instead, and add `--cleanup`
if we want to clean up the folder after.

```bash
$ urlchecker check https://github.com/SuperKogito/SuperKogito.github.io.git
```

If you specify any arguments for a white list (or any kind of expected list) make
sure that you provide a comma separated list *without any spaces*

```bash
$ urlchecker check --exclude-files=README.md,_config.yml
```

### Save Results

If you want to save your results to file, perhaps for some kind of record or
other data analysis, you can provide the `--save` argument:

```bash
$ urlchecker check --save results.csv .
```

The file that you save to will include a comma separated value tabular listing
of the urls, and their result. The result options are "passed" and "failed"
and the default header is `URL,RESULT`. All of these defaults are exposed
if you want to change them (e.g., using a tab separator or a different header)
if you call the function from within Python. Here is an example of the default file
produced, which should satisfy most use cases:

```
URL,RESULT
https://github.com/SuperKogito,passed
https://www.google.com/,passed
https://github.com/SuperKogito/Voice-based-gender-recognition/issues,passed
https://github.com/SuperKogito/Voice-based-gender-recognition,passed
https://github.com/SuperKogito/spafe/issues/4,passed
https://github.com/SuperKogito/Voice-based-gender-recognition/issues/2,passed
https://github.com/SuperKogito/spafe/issues/5,passed
https://github.com/SuperKogito/URLs-checker/blob/master/README.md,passed
https://img.shields.io/,passed
https://github.com/SuperKogito/spafe/,passed
https://github.com/SuperKogito/spafe/issues/3,passed
https://www.google.com/,passed
https://github.com/SuperKogito,passed
https://github.com/SuperKogito/spafe/issues/8,passed
https://github.com/SuperKogito/spafe/issues/7,passed
https://github.com/SuperKogito/Voice-based-gender-recognition/issues/1,passed
https://github.com/SuperKogito/spafe/issues,passed
https://github.com/SuperKogito/URLs-checker/issues,passed
https://github.com/SuperKogito/spafe/issues/2,passed
https://github.com/SuperKogito/URLs-checker,passed
https://github.com/SuperKogito/spafe/issues/6,passed
https://github.com/SuperKogito/spafe/issues/1,passed
https://github.com/SuperKogito/URLs-checker/README.md,failed
https://github.com/SuperKogito/URLs-checker/issues/3,failed
https://none.html,failed
https://github.com/SuperKogito/URLs-checker/issues/2,failed
https://github.com/SuperKogito/URLs-checker/README.md,failed
https://github.com/SuperKogito/URLs-checker/issues/1,failed
https://github.com/SuperKogito/URLs-checker/issues/4,failed
```


### Usage from Python

#### Checking a Path

If you want to check a list of urls outside of the provided client, this is fairly easy to do!
Let's say we have a path, our present working directory, and we want to check
.py and .md files (the default)

```python
from urlchecker.core.check import UrlChecker
import os

path = os.getcwd()
checker = UrlChecker(path)    
# UrlChecker:/home/vanessa/Desktop/Code/urlstechie/urlchecker-python
```

And of course you can provide more substantial arguments to derive the original
file list:

```python
checker = UrlChecker(
    path=path,
    file_types=[".md", ".py", ".rst"],
    include_patterns=[],
    exclude_files=["README.md", "LICENSE"],
    print_all=True,
)
```
I can then run the checker like this:

```python
checker.run()
```

Or with more customization of excluded urls:

```python
checker.run(
    exclude_urls=exclude_urls,
    exclude_patterns=exclude_patterns,
    retry_count=3,
    timeout=5,
)
```

You'll get the results object returned, which is also available at `checker.results`,
a simple dictionary with "passed" and "failed" keys to show passes and fails across
all files.

```python
{'passed': ['https://github.com/SuperKogito/spafe/issues/4',
  'http://shachi.org/resources',
  'https://superkogito.github.io/blog/SpectralLeakageWindowing.html',
  'https://superkogito.github.io/figures/fig4.html',
  'https://github.com/urlstechie/urlchecker-test-repo',
  'https://www.google.com/',
  ...
  'https://github.com/SuperKogito',
  'https://img.shields.io/',
  'https://www.google.com/',
  'https://docs.python.org/2'],
 'failed': ['https://github.com/urlstechie/urlschecker-python/tree/master',
  'https://github.com/SuperKogito/Voice-based-gender-recognition,passed',
  'https://github.com/SuperKogito/URLs-checker/README.md',
   ...
  'https://superkogito.github.io/tables',
  'https://github.com/SuperKogito/URLs-checker/issues/2',
  'https://github.com/SuperKogito/URLs-checker/README.md',
  'https://github.com/SuperKogito/URLs-checker/issues/4',
  'https://github.com/SuperKogito/URLs-checker/issues/3',
  'https://github.com/SuperKogito/URLs-checker/issues/1',
  'https://none.html']}
```

You can look at `checker.checks`, which is a dictionary of result objects,
organized by the filename:

```python
for file_name, result in checker.checks.items(): 
    print() 
    print(result) 
    print("Total Results: %s " % result.count) 
    print("Total Failed: %s" % len(result.failed)) 
    print("Total Passed: %s" % len(result.passed)) 

...

UrlCheck:/home/vanessa/Desktop/Code/urlstechie/urlchecker-python/tests/test_files/sample_test_file.md
Total Results: 26 
Total Failed: 6
Total Passed: 20

UrlCheck:/home/vanessa/Desktop/Code/urlstechie/urlchecker-python/.pytest_cache/README.md
Total Results: 1 
Total Failed: 0
Total Passed: 1

UrlCheck:/home/vanessa/Desktop/Code/urlstechie/urlchecker-python/.eggs/pytest_runner-5.2-py3.7.egg/ptr.py
Total Results: 0 
Total Failed: 0
Total Passed: 0

UrlCheck:/home/vanessa/Desktop/Code/urlstechie/urlchecker-python/docs/source/conf.py
Total Results: 3 
Total Failed: 0
Total Passed: 3
```

For any result object, you can print the list of passed, falied, white listed,
or all the urls.

```python
result.all                                                                                                                                                                       
['https://www.sphinx-doc.org/en/master/usage/configuration.html',
 'https://docs.python.org/3',
 'https://docs.python.org/2']

result.failed                                                                                                                                                                    
[]

result.exclude
[]

result.passed                                                                                                                                                                    
['https://www.sphinx-doc.org/en/master/usage/configuration.html',
 'https://docs.python.org/3',
 'https://docs.python.org/2']

result.count
3
```


#### Checking a List of URls

If you start with a list of urls you want to check, you can do that too!

```python
from urlchecker.core.urlproc import UrlCheckResult

urls = ['https://www.github.com', "https://github.com", "https://banana-pudding-doesnt-exist.com"]

# Instantiate an empty checker to extract urls
checker = UrlCheckResult()
File name None is undefined or does not exist, skipping extraction.
```

If you provied a file name, the urls would be extracted for you.

```python
checker = UrlCheckResult(
    file_name=file_name,
    exclude_patterns=exclude_patterns,
    exclude_urls=exclude_urls,
    print_all=self.print_all,
)
```

or you can provide all the parameters without the filename:

```python
checker = UrlCheckResult(
    exclude_patterns=exclude_patterns,
    exclude_urls=exclude_urls,
    print_all=self.print_all,
)
```

If you don't provide the file_name to check urls, you can give the urls
you defined previously directly to the `check_urls` function:


```python
checker.check_urls(urls)

https://www.github.com
https://github.com
HTTPSConnectionPool(host='banana-pudding-doesnt-exist.com', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f989abdfa10>: Failed to establish a new connection: [Errno -2] Name or service not known'))
https://banana-pudding-doesnt-exist.com
```

And of course you can specify a timeout and retry:

```python
checker.check_urls(urls, retry_count=retry_count, timeout=timeout)
```

After you run the checker you can get all the urls, the passed,
and failed sets:

```python
checker.failed                                                                                                                                                                   
['https://banana-pudding-doesnt-exist.com']

checker.passed                                                                                                                                                                   
['https://www.github.com', 'https://github.com']

checker.all                                                                                                                                                                      
['https://www.github.com',
 'https://github.com',
 'https://banana-pudding-doesnt-exist.com']

checker.all                                                                                                                                                                      
['https://www.github.com',
 'https://github.com',
 'https://banana-pudding-doesnt-exist.com']

checker.count                                                                                                                                                                    
3
```

If you have any questions, please don't hesitate to [open an issue](https://github.com/urlstechie/urlchecker-python).

### Docker

A Docker container is provided if you want to build a base container with urlchecker,
meaning that you don't need to install it on your host. You can build the container as
follows:

```bash
docker build -t urlchecker .
```

And then the entrypoint will expose the urlchecker.

```bash
docker run -it urlschecker
```

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

## Support

If you need help, or want to suggest a project for the organization,
please [open an issue](https://github.com/urlstechie/urlchecker-python)
