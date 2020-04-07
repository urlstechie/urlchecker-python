#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
import subprocess
import configparser
from urlchecker.logger import print_failure
from urlchecker.core.fileproc import get_file_paths
from urlchecker.main.github import clone_repo, delete_repo
from urlchecker.core.check import check_files, run_urlchecker


@pytest.mark.parametrize('local_folder_path', ['./tests/test_files'])
@pytest.mark.parametrize('config_fname', ['./tests/_local_test_config.conf'])
@pytest.mark.parametrize('white_listed_files', [[], ['./tests/test_files/sample_test_file.py']])
def test_locally(local_folder_path, config_fname, white_listed_files):
    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # read input variables
    file_types = config['DEFAULT']["file_types_test_values"].split(",")
    print_all = True
    white_listed_urls = config['DEFAULT']["white_listed_test_urls"].split(",")
    white_listed_patterns = config['DEFAULT']["white_listed__test_patterns"].split(",")

    # debug prints
    print(" config")
    print(" -------")
    print("%25s : %10s" % ("path", local_folder_path))
    print("%25s : %10s" % ("file_types", file_types))
    print("%25s : %10s" % ("white_listed_files", white_listed_files))
    print("%25s : %10s" % ("white_listed_urls", white_listed_urls))
    print("%25s : %10s" % ("white_listed_patterns", white_listed_patterns))

    run_urlchecker(local_folder_path,
                   file_types,
                   white_listed_files,
                   white_listed_urls,
                   white_listed_patterns,
                   print_all)


@pytest.mark.parametrize('retry_count', [1, 3])
def test_check_generally(retry_count):

    # init vars
    git_path = "https://github.com/urlstechie/urlchecker-test-repo"
    file_types = [".py", ".md"]
    print_all = True
    white_listed_urls = ["https://superkogito.github.io/figures/fig2.html",
                         "https://superkogito.github.io/figures/fig4.html"]
    white_listed_patterns = ["https://superkogito.github.io/tables"]
    timeout = 1
    force_pass = False

    print(os.path.exists(os.path.basename(git_path)), os.path.basename(git_path))
    # del repo if it exisits
    if os.path.exists(os.path.basename(git_path)):
        delete_repo(os.path.basename(git_path))

    # clone repo
    base_path = clone_repo(git_path)

    # get all file paths
    file_paths = get_file_paths(base_path, file_types)

    # check repo urls
    check_results = check_files(file_paths, print_all, white_listed_urls,
                                white_listed_patterns, retry_count, timeout)

    # exit
    if not check_results['failed'] and not check_results['passed']:
        print("\n\nDone. No links were collected.")
        sys.exit(0)

    elif not force_pass and check_results['failed']:
        print("\n\nDone. The following URLS did not pass:")
        for failed_url in check_results['failed']:
            print_failure(failed_url)
        if retry_count == 1:
            return True
    else:
        print("\n\nDone. All URLS passed.")
        if retry_count == 3:
            return True
