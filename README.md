# urlchecker python

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/urlstechie/urlchecker-python/blob/master/LICENSE)

![docs/urlstechie.png](docs/urlstechie.png)

This is a python module to collect urls over static files (code and documentation)
and then test for and report broken links.

## Module Documentation

A detailed documentation of the code is available under [urls-checker.readthedocs.io](https://urls-checker.readthedocs.io/en/latest/)

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

$ urlchecker check --help
usage: urlchecker check [-h] [-b BRANCH] [--subfolder SUBFOLDER] [--cleanup]
                        [--force-pass] [--no-print] [--file-types FILE_TYPES]
                        [--white-listed-urls WHITE_LISTED_URLS]
                        [--white-listed-patterns WHITE_LISTED_PATTERNS]
                        [--white-listed-files WHITE_LISTED_FILES]
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
  --white-listed-urls WHITE_LISTED_URLS
                        comma separated list of white listed urls (no spaces)
  --white-listed-patterns WHITE_LISTED_PATTERNS
                        comma separated list of white listed patterns for urls
                        (no spaces)
  --white-listed-files WHITE_LISTED_FILES
                        comma separated list of white listed files and
                        patterns for files (no spaces)
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
      print all: True
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

If you have any questions, please don't hesitate to [open an issue](https://github.com/urlstechie/urlchecker-python).


### Docker

A Docker container is provided if you want to build a base container with urlchecker,
meaning that you don't need to install it on your host. You can build the container as 
follows:

```bsah
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
