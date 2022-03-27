from urlchecker.core.exclude import excluded


def test_whitelisted():
    """
    test excluded function
    """
    url = "https://excluded/subpage"

    # Not in excluded
    assert not excluded(url)

    # Exact url provided as excluded
    assert excluded(url, [url])

    # Pattern provided as white list
    assert excluded(url, [], ["https://excluded/"])
