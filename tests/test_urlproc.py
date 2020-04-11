#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
from urlchecker.core.fileproc import collect_links_from_file
from urlchecker.core.urlproc import UrlCheckResult


@pytest.mark.parametrize(
    "file",
    ["tests/test_files/sample_test_file.md", "tests/test_files/sample_test_file.py"],
)
def test_check_urls(file):
    """
    test check urls check function.
    """
    urls = collect_links_from_file(file)
    checker = UrlCheckResult()
    checker.check_urls(urls)
