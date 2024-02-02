import os
import re
import sys
import pytest
import configparser
from urlchecker.core.fileproc import get_file_paths
from urlchecker.main.github import clone_repo
from urlchecker.core.check import UrlChecker


@pytest.mark.parametrize(
    "file_paths",
    [
        ["tests/test_files/sample_test_file.md"],
        ["tests/test_files/sample_test_file.py"],
        ["tests/test_files/sample_test_file.rst"],
    ],
)
@pytest.mark.parametrize("print_all", [False, True])
@pytest.mark.parametrize(
    "exclude_urls", [["https://github.com/SuperKogito/SuperKogito.github.io"]]
)
@pytest.mark.parametrize(
    "exclude_patterns",
    [[], ["https://github.com/SuperKogito/SuperKogito.github.io"]],
)
def test_check_files(file_paths, print_all, exclude_urls, exclude_patterns):
    """
    test check repo function.
    """
    checker = UrlChecker(print_all=print_all)
    checker.run(
        file_paths,
        exclude_urls=exclude_urls,
        exclude_patterns=exclude_patterns,
        retry_count=1,
    )


@pytest.mark.parametrize("file_paths", [["tests/test_files/hard_urls.md"]])
def test_difficult_urls(file_paths):
    """
    test difficult urls that likely require selenium.
    """
    checker = UrlChecker()
    results = checker.run(file_paths, timeout=120)

    # This should be the only failing (503)
    print("Failed URLs:", results["failed"])

    assert "https://thisurldoesnotexist-pancakes.whatever" in results["failed"]
    working = [
        "https://www.hpcwire.com/2019/01/17/pfizer-hpc-engineer-aims-to-automate-software-stack-testing/",
        "https://www.sciencedirect.com/science/article/pii/S0013468608005045",
        "https://doi.org/10.1063/5.0023771",
        "https://www.linux.org/",
        "https://drupal.org/",
        "https://codepen.io/rootwork/",
        "http://groundwire.org/blog/groundwire-engagement-pyramid/",
        "https://twig.symfony.com/doc/",
        "https://groups.drupal.org/node/298298",
        "https://portland2013.drupal.org/program/sprints.html",
        "https://twitter.com/wharman",
        "https://www.progressiveexchange.org",
        "https://twitter.com/jooy8/status/322734500226412544",
        "https://www.drupal.org/node/1982024",
        "https://groups.drupal.org/node/278968",
    ]
    for url in working:
        assert url in results["passed"]


@pytest.mark.parametrize("local_folder_path", ["./tests/test_files"])
@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
def test_locally(local_folder_path, config_fname):
    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # read input variables
    git_path = local_folder_path
    file_types = config["DEFAULT"]["file_types_test_values"].split(",")
    print_all = True
    exclude_urls = config["DEFAULT"]["exclude_test_urls"].split(",")
    exclude_patterns = config["DEFAULT"]["exclude_test_patterns"].split(",")

    # get all file paths
    file_paths = get_file_paths(git_path, file_types)

    # check repo urls
    checker = UrlChecker(print_all=print_all)
    checker.run(
        file_paths=file_paths,
        exclude_urls=exclude_urls,
        exclude_patterns=exclude_patterns,
        retry_count=1,
    )
    print("Done.")


@pytest.mark.parametrize("retry_count", [1, 3])
def test_check_run_save(tmp_path, retry_count):

    # init vars
    git_path = "https://github.com/urlstechie/urlchecker-test-repo"
    file_types = [".py", ".md"]
    print_all = True
    exclude_urls = [
        "https://superkogito.github.io/figures/fig2.html",
        "https://superkogito.github.io/figures/fig4.html",
    ]
    exclude_patterns = ["https://superkogito.github.io/tables"]
    timeout = 1
    force_pass = False

    # clone repo
    base_path = clone_repo(git_path)

    # get all file paths in subfolder specified
    base_path = os.path.join(base_path, "test_files")
    file_paths = get_file_paths(base_path, file_types)

    # check repo urls
    checker = UrlChecker(print_all=print_all)
    check_results = checker.run(
        file_paths=file_paths,
        exclude_urls=exclude_urls,
        exclude_patterns=exclude_patterns,
        retry_count=retry_count,
        timeout=timeout,
    )

    # Test saving to file
    output_file = os.path.join(str(tmp_path), "results.csv")
    assert not os.path.exists(output_file)
    saved_file = checker.save_results(output_file)
    assert os.path.exists(output_file)

    # Read in output file
    with open(saved_file, "r") as filey:
        lines = filey.readlines()

    # Header line has three items
    assert lines[0] == "URL,RESULT,FILENAME\n"

    # Ensure content looks okay
    for line in lines[1:]:
        url, result, filename = line.split(",")

        root = filename.split("/")[0]
        assert url.startswith("http")
        assert result in ["passed", "failed"]
        assert re.search("(.py|.md)$", filename)

    # Save with full path
    saved_file = checker.save_results(output_file, relative_paths=False)

    # Read in output file
    with open(saved_file, "r") as filey:
        lines = filey.readlines()

    # Ensure content looks okay
    for line in lines[1:]:
        url, result, filename = line.split(",")
        assert not filename.startswith(root)
