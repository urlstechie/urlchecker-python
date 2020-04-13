import pytest
from urlchecker.core.fileproc import collect_links_from_file
from urlchecker.core.urlproc import (
    UrlCheckResult,
    get_user_agent,
    check_response_status_code,
)


@pytest.mark.parametrize(
    "file", ["tests/test_files/sample_test_file.md"],
)
def test_check_urls(file):
    """
    test check urls check function.
    """
    urls = collect_links_from_file(file)
    checker = UrlCheckResult()
    assert str(checker) == "UrlCheckResult"

    # Checker should have passed, failed, and all
    for attribute in ["passed", "failed", "all"]:
        assert hasattr(checker, attribute)

    assert not checker.passed
    assert not checker.failed
    assert not checker.all
    checker.check_urls(urls)

    # Ensure we have the correct sums for passing/failing
    assert len(checker.failed + checker.passed) == checker.count
    assert len(checker.all) == len(urls)

    # Ensure one not whitelisted is failed
    assert "https://github.com/SuperKogito/URLs-checker/issues/1" in checker.failed

    # Run again with whitelist of exact urls
    checker = UrlCheckResult(
        white_listed_urls=["https://github.com/SuperKogito/URLs-checker/issues/1"]
    )
    checker.check_urls(urls)
    assert (
        "https://github.com/SuperKogito/URLs-checker/issues/1" in checker.white_listed
    )

    # Run again with whitelist of patterns
    checker = UrlCheckResult(
        white_listed_patterns=["https://github.com/SuperKogito/URLs-checker/issues"]
    )
    checker.check_urls(urls)
    for failed in checker.failed:
        assert not failed.startswith(
            "https://github.com/SuperKogito/URLs-checker/issues"
        )


def test_get_user_agent():
    user_agent = get_user_agent()
    assert isinstance(user_agent, str)


@pytest.mark.parametrize(
    "print_level", ["all", "only_files_with_urls",
                    "fails-only", "success-only", "none"]
)
def test_check_response_status_code(print_level):
    class failedResponse:
        status_code = 500

    class successResponse:
        status_code = 200

    # Any failure returns True (indicating a retry is needed)
    assert not check_response_status_code(
        "https://this-should-succeed", successResponse, print_level
    )
    assert check_response_status_code("https://this-should-fail", failedResponse, print_level)
    assert check_response_status_code("https://this-should-also-fail", None, print_level)
