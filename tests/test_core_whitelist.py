import pytest
from urlchecker.core.whitelist import white_listed


def test_whitelisted():
    """
    test whitelisted function
    """
    url = "https://white-listed/subpage"

    # Not in any whitelist
    assert not white_listed(url)

    # Exact url provided as white list url
    assert white_listed(url, [url])

    # Pattern provided as white list
    assert white_listed(url, [], ["https://white-listed/"])
