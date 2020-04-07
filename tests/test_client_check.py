#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pytest
import tempfile
import subprocess
import configparser
from types import SimpleNamespace
from urlchecker.client.check import main


def test_installation():
    # test installation
    install_cmd = ["pip3", "install", "."]

    # install script
    pipe = subprocess.run(install_cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    if pipe.stderr:
        print("ERROR")
        print(pipe.stderr)
        raise AssertionError


@pytest.mark.parametrize('config_fname', ['./tests/_local_test_config.conf'])
@pytest.mark.parametrize('print_all', [False, True])
@pytest.mark.parametrize('force_pass', [False, True])
@pytest.mark.parametrize('rcount', [1, 3])
@pytest.mark.parametrize('timeout', [3, 5])
@pytest.mark.parametrize('save', ["", "./tests/test_results.csv"])
def test_script(config_fname, print_all, force_pass, rcount, timeout, save):
    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # init env variables
    path = config['DEFAULT']["git_path_test_value"]
    file_types = config['DEFAULT']["file_types_test_values"]
    white_listed_urls = config['DEFAULT']["white_listed_test_urls"]
    white_listed_patterns =  config['DEFAULT']["white_listed__test_patterns"]
    branch = "master"

    # avoid redundant cloning
    if os.path.exists("urlchecker-test-repo"):
        path = "urlchecker-test-repo"
        branch = ""

    # define args
    args = SimpleNamespace(branch=branch, cleanup=True, command='check',
                           debug=False, file_types='.md,.py', force_pass=force_pass,
                           no_print=not print_all, path=path, retry_count=rcount, save=save,
                           subfolder=None, timeout=timeout, version=False,
                           white_listed_files="conf.py",
                           white_listed_patterns=white_listed_patterns,
                           white_listed_urls=white_listed_urls)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(args=args, extra="")

    if force_pass:
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
    else :
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    # clean up after test
    if save != "":
        os.remove(save)

    # # make sure test repo is deleted when done
    # if os.path.exists("urlchecker-test-repo"):
    #     os.remove("urlchecker-test-repo")


def test_uninstallation():
    # uninstall lib
    uninstall_cmd = ["pip3", "uninstall", "urlchecker", "--y"]

    # install script
    pipe = subprocess.run(uninstall_cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    if pipe.stderr:
        print("ERROR")
        print(pipe.stderr)
        raise AssertionError
