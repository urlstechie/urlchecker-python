#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
from urlchecker.core.whitelist import white_listed


@pytest.mark.parametrize('test_url', ["https://github.com/SuperKogito/spafe/issues/1"
                                      "https://github.com/SuperKogito/spafe/issues/2",
                                      "https://github.com/SuperKogito/spafe/issues/3"])
@pytest.mark.parametrize('white_listed_test_urls', [[], ["https://github.com/SuperKogito/spafe/issues/2"]])
@pytest.mark.parametrize('white_listed_test_patterns', [[], ["https://github.com/SuperKogito/spafe/issues/"]])
def test_white_listed(test_url, white_listed_test_urls, white_listed_test_patterns):
    """
    test white listing urls
    """
    output = white_listed(test_url,
                          white_listed_test_urls,
                          white_listed_test_patterns)

    # bool for whether link is in filter lists
    in_urls_whitelist = (test_url in white_listed_test_patterns)
    in_patterns_whitelist = (True in [True if pattern in test_url else False
                                      for pattern in white_listed_test_patterns])

    # check output is similar to expected result
    if output != (in_urls_whitelist or in_patterns_whitelist):
        raise AssertionError
