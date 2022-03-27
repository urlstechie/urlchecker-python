import pytest
from urlchecker.core.fileproc import collect_links_from_file
from urlchecker.core.urlproc import (
    UrlCheckResult,
    find_urls,
    get_user_agent,
    check_response_status_code,
)


@pytest.mark.parametrize(
    "files",
    [
        [
            "tests/test_files/sample_test_file.md",
            "tests/test_files/sample_test_file.py",
            "tests/test_files/sample_test_file.rst",
        ]
    ],
)
def test_no_duplicates(files):
    """
    Ensure when we provide a list of files (with redundant urls) we don't
    see duplicates when using find_urls
    """
    seen = set()
    for _, urls in find_urls(files):
        for url in urls:
            assert url not in seen
        [seen.add(url) for url in urls]


@pytest.mark.parametrize(
    "filename",
    ["tests/test_files/sample_test_file.md"],
)
def test_check_urls(filename):
    """
    test check urls check function.
    """
    urls = collect_links_from_file(filename)
    checker = UrlCheckResult()
    assert str(checker) == "UrlCheckResult"

    # Checker should have passed, failed, and all
    for attribute in ["passed", "failed", "all"]:
        assert hasattr(checker, attribute)

    assert not checker.passed
    assert not checker.failed
    assert not checker.all
    assert not checker.excluded
    checker.check_urls(urls)

    # Ensure we have the correct sums for passing/failing
    assert len(checker.failed + checker.passed + checker.excluded) == checker.count
    assert len(checker.all) == len(urls)

    # Ensure one not excluded is failed
    assert "https://none.html" in checker.failed

    assert checker.print_all

    # Run again with excluded exact urls
    checker = UrlCheckResult(exclude_urls=["https://none.html"])
    checker.check_urls(urls)
    assert "https://none.html" in checker.excluded

    # Run again with exclude of patterns
    checker = UrlCheckResult(
        exclude_patterns=["https://github.com/SuperKogito/URLs-checker/issues"]
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
