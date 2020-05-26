<div style="text-align:center"><img src="https://raw.githubusercontent.com/urlstechie/urlchecker-python/master/docs/urlstechie.png"/></div>

[![Build Status](https://travis-ci.com/urlstechie/urlchecker-python.svg?branch=master)](https://travis-ci.com/urlstechie/urlchecker-python) [![Documentation Status](https://readthedocs.org/projects/urlchecker-python/badge/?version=latest)](https://urlchecker-python.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/urlstechie/urlchecker-python/branch/master/graph/badge.svg)](https://codecov.io/gh/urlstechie/urlchecker-python) [![Python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue)](https://www.python.org/doc/versions/) [![CodeFactor](https://www.codefactor.io/repository/github/urlstechie/urlchecker-python/badge)](https://www.codefactor.io/repository/github/urlstechie/urlchecker-python) ![PyPI](https://img.shields.io/pypi/v/urlchecker) [![Downloads](https://pepy.tech/badge/urlchecker)](https://pepy.tech/project/urlchecker) [![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/urlstechie/urlchecker-python/blob/master/LICENSE)


# urlchecker-python

This is a python module to collect urls over static files (code and documentation)
and then test for and report broken links. If you are interesting in using
this as a GitHub action, see [urlchecker-action](https://github.com/urlstechie/urlchecker-action). There are also container
bases available on [quay.io/urlstechie/urlchecker](https://quay.io/repository/urlstechie/urlchecker?tab=tags).

## Module Documentation

A detailed documentation of the code is available under [urlchecker-python.readthedocs.io](https://urlchecker-python.readthedocs.io/en/latest/)

## Usage

### Install

You can install the urlchecker from [pypi](https://pypi.org/project/urlchecker):

```bash
pip install urlchecker
```

or install from the repository directly:

```bash
git clone https://github.com/urlstechie/urlchecker-python.git
cd urlchecker-python
python setup.py install
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
                        [--force-pass] [--file-types FILE_TYPES]
                        [--files FILES] [--print-level PRINT_LEVEL]
                        [--white-listed-urls WHITE_LISTED_URLS]
                        [--white-listed-patterns WHITE_LISTED_PATTERNS]
                        [--white-listed-files WHITE_LISTED_FILES]
                        [--save SAVE] [--retry-count RETRY_COUNT]
                        [--timeout TIMEOUT]
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
  --file-types FILE_TYPES
                        comma separated list of file extensions to check
                        (defaults to .md,.py)
  --files FILES         comma separated list of exact files or patterns to
                        check.
  --print-level PRINT_LEVEL
                        print levels: all, files-with-urls-only, fails-only,
                        success-only, none
  --white-listed-urls WHITE_LISTED_URLS
                        comma separated list of white listed urls (no spaces)
  --white-listed-patterns WHITE_LISTED_PATTERNS
                        comma separated list of white listed patterns for urls
                        (no spaces)
  --white-listed-files WHITE_LISTED_FILES
                        comma separated list of white listed files and
                        patterns for files (no spaces)
  --save SAVE           Path to a csv file to save results to.
  --retry-count RETRY_COUNT
                        retry count upon failure (defaults to 2, one retry).
  --timeout TIMEOUT     timeout (seconds) to provide to the requests library
                        (defaults to 5)
```

You have a lot of flexibility to define patterns of urls or files to skip,
along with the number of retries or timeout (seconds). The most basic usage will
check an entire directory. Let's clone and check the directory of one of the
maintainers:

```bash
git clone https://github.com/SuperKogito/SuperKogito.github.io.git
cd SuperKogito.github.io
urlchecker check .

$ urlchecker check .
  original path: .
     final path: /tmp/SuperKogito.github.io
      subfolder: None
         branch: master
        cleanup: False
     file types: ['.md', '.py']
    print level: all
 url whitetlist: []
   url patterns: []
  file patterns: []
     force pass: False
    retry count: 2
        timeout: 5

 /tmp/SuperKogito.github.io/README.md
 ------------------------------------
https://travis-ci.com/SuperKogito/SuperKogito.github.io
https://www.python.org/download/releases/3.0/
https://superkogito.github.io/blog/diabetesML2.html
https://superkogito.github.io/blog/Cryptography.html
http://www.sphinx-doc.org/en/master/
https://github.com/
https://superkogito.github.io/blog/SignalFraming.html
https://superkogito.github.io/blog/VoiceBasedGenderRecognition.html
https://travis-ci.com/SuperKogito/SuperKogito.github.io.svg?branch=master
https://superkogito.github.io/blog/SpectralLeakageWindowing.html
https://superkogito.github.io/blog/Intro.html
https://github.com/SuperKogito/SuperKogito.github.io/workflows/Check%20URLs/badge.svg
https://superkogito.github.io/blog/diabetesML1.html
https://superkogito.github.io/blog/AuthenticatedEncryption.html
https://superKogito.github.io/blog/ffmpegpipe.html
https://superkogito.github.io/blog/Encryption.html
https://superkogito.github.io/blog/NaiveVad.html

 /tmp/SuperKogito.github.io/_project/src/postprocessing.py
 ---------------------------------------------------------
No urls found.
...

https://github.com/marsbroshok/VAD-python/blob/d74033aa08fbbbcdbd491f6e52a1dfdbbb388eea/vad.py#L64
https://github.com/fgnt/pb_chime5
https://ai.facebook.com/blog/wav2vec-state-of-the-art-speech-recognition-through-self-supervision/
https://corplinguistics.wordpress.com/tag/mandarin/
http://www.cs.tut.fi/~tuomasv/papers/ijcnn_paper_valenti_extended.pdf
http://shachi.org/resources
https://conference.scipy.org/proceedings/scipy2015/pdfs/brian_mcfee.pdf
https://www.dlology.com/blog/simple-speech-keyword-detecting-with-depthwise-separable-convolutions/
https://stackoverflow.com/questions/49197916/how-to-profile-cpu-usage-of-a-python-script


Done. All URLS passed.
```

### Check GitHub Repository

But wouldn't it be easier to not have to clone the repository first?
Of course! We can specify a GitHub url instead, and add `--cleanup`
if we want to clean up the folder after.

```bash
urlchecker check https://github.com/SuperKogito/SuperKogito.github.io.git
```

If you specify any arguments for a white list (or any kind of expected list) make
sure that you provide a comma separated list *without any spaces*

```
urlchecker check --white-listed-files=README.md,_config.yml
```

### Save Results

If you want to save your results to file, perhaps for some kind of record or
other data analysis, you can provide the `--save` argument:

```bash
$ urlchecker check --save results.csv .
  original path: .
     final path: /home/vanessa/Desktop/Code/urlstechie/urlchecker-test-repo
      subfolder: None
         branch: master
        cleanup: False
     file types: ['.md', '.py']
    print level: all
 url whitetlist: []
   url patterns: []
  file patterns: []
     force pass: False
    retry count: 2
           save: results.csv
        timeout: 5

 /home/vanessa/Desktop/Code/urlstechie/urlchecker-test-repo/README.md
 --------------------------------------------------------------------
No urls found.

 /home/vanessa/Desktop/Code/urlstechie/urlchecker-test-repo/test_files/sample_test_file.py
 -----------------------------------------------------------------------------------------
https://github.com/SuperKogito/URLs-checker/README.md
https://github.com/SuperKogito/URLs-checker/README.md
https://www.google.com/
https://github.com/SuperKogito

 /home/vanessa/Desktop/Code/urlstechie/urlchecker-test-repo/test_files/sample_test_file.md
 -----------------------------------------------------------------------------------------
https://github.com/SuperKogito/URLs-checker/blob/master/README.md
https://github.com/SuperKogito/Voice-based-gender-recognition/issues
https://github.com/SuperKogito/spafe/issues/7
https://github.com/SuperKogito/URLs-checker
https://github.com/SuperKogito/URLs-checker/issues
https://github.com/SuperKogito/spafe/issues/4
https://github.com/SuperKogito/URLs-checker/issues/2
https://github.com/SuperKogito/URLs-checker/issues/2
https://github.com/SuperKogito/Voice-based-gender-recognition/issues/1
https://github.com/SuperKogito/spafe/issues/6
https://github.com/SuperKogito/spafe/issues
...

Saving results to /home/vanessa/Desktop/Code/urlstechie/urlchecker-test-repo/results.csv


Done. All URLS passed.
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
    white_listed_files=["README.md", "LICENSE"],
    print_level="all",
)
```
I can then run the checker like this:

```python
checker.run()
```

Or with more customization of white listing urls:

```python
checker.run(
    white_listed_urls=white_listed_urls,
    white_listed_patterns=white_listed_patterns,
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

result.white_listed
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
    white_listed_patterns=white_listed_patterns,
    white_listed_urls=white_listed_urls,
    print_level=self.print_level,
)
```

or you can provide all the parameters without the filename:

```python
checker = UrlCheckResult(
    white_listed_patterns=white_listed_patterns,
    white_listed_urls=white_listed_urls,
    print_level=self.print_level,
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
