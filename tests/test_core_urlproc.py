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
    assert not checker.white_listed
    checker.check_urls(urls)

    # Ensure we have the correct sums for passing/failing
    assert len(checker.failed + checker.passed + checker.white_listed) == checker.count
    assert len(checker.all) == len(urls)

    # Ensure one not whitelisted is failed
    assert "https://none.html" in checker.failed

    assert checker.print_all

    # Run again with whitelist of exact urls
    checker = UrlCheckResult(
        white_listed_urls=["https://none.html"]
    )
    checker.check_urls(urls)
    assert (
        "https://none.html" in checker.white_listed
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


def test_check_response_status_code():
    class failedResponse:
        status_code = 500

    class successResponse:
        status_code = 200

    # Any failure returns True (indicating a retry is needed)
    assert not check_response_status_code(
        "https://this-should-succeed", successResponse
    )
    assert check_response_status_code("https://this-should-fail", failedResponse)
    assert check_response_status_code("https://this-should-also-fail", None)
