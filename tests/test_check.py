import os
import re
import sys
import pytest
import subprocess
import tempfile
import configparser
from urlchecker.core.fileproc import get_file_paths
from urlchecker.main.github import clone_repo
from urlchecker.core.check import UrlChecker
from urlchecker.logger import print_failure


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
    "white_listed_urls", [["https://github.com/SuperKogito/SuperKogito.github.io"]]
)
@pytest.mark.parametrize(
    "white_listed_patterns",
    [[], ["https://github.com/SuperKogito/SuperKogito.github.io"]],
)
def test_check_files(file_paths, print_all, white_listed_urls, white_listed_patterns):
    """
    test check repo function.
    """
    checker = UrlChecker(print_all=print_all)
    checker.run(
        file_paths,
        white_listed_urls=white_listed_urls,
        white_listed_patterns=white_listed_patterns,
    )


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_all", [False, True])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1, 3])
@pytest.mark.parametrize("timeout", [3, 5])
def test_script(config_fname, cleanup, print_all, force_pass, rcount, timeout):
    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # init env variables
    path = config["DEFAULT"]["git_path_test_value"]
    file_types = config["DEFAULT"]["file_types_test_values"]
    white_listed_urls = config["DEFAULT"]["white_listed_test_urls"]
    white_listed_patterns = config["DEFAULT"]["white_listed__test_patterns"]

    # Generate command
    cmd = [
        "urlchecker",
        "check",
        "--subfolder",
        "test_files",
        "--file-types",
        file_types,
        "--white-listed-files",
        "conf.py",
        "--white-listed-urls",
        white_listed_urls,
        "--white-listed_patterns",
        white_listed_patterns,
        "--retry-count",
        str(rcount),
        "--timeout",
        str(timeout),
    ]

    # Add boolean arguments
    if cleanup:
        cmd.append("--cleanup")
    if print_all:
        cmd.append("--print-all")
    if force_pass:
        cmd.append("--force-pass")

    # Add final path
    cmd.append(path)

    # excute script
    pipe = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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
    white_listed_urls = config["DEFAULT"]["white_listed_test_urls"].split(",")
    white_listed_patterns = config["DEFAULT"]["white_listed__test_patterns"].split(",")

    # debug prints
    print(" config")
    print(" -------")
    print("%25s : %10s" % ("git_path", git_path))
    print("%25s : %10s" % ("file_types", file_types))
    print("%25s : %10s" % ("white_listed_urls", white_listed_urls))
    print("%25s : %10s" % ("white_listed_patterns", white_listed_patterns))

    # get all file paths
    file_paths = get_file_paths(git_path, file_types)

    # check repo urls
    checker = UrlChecker(print_all=print_all)
    checker.run(
        file_paths=file_paths,
        white_listed_urls=white_listed_urls,
        white_listed_patterns=white_listed_patterns,
    )
    print("Done.")


@pytest.mark.parametrize("retry_count", [1, 3])
def test_check_run_save(tmp_path, retry_count):

    # init vars
    git_path = "https://github.com/urlstechie/urlchecker-test-repo"
    file_types = [".py", ".md"]
    print_all = True
    white_listed_urls = [
        "https://superkogito.github.io/figures/fig2.html",
        "https://superkogito.github.io/figures/fig4.html",
    ]
    white_listed_patterns = ["https://superkogito.github.io/tables"]
    timeout = 1
    force_pass = False

    # clone repo
    base_path = clone_repo(git_path)

    # get all file paths in subfolder specified
    base_path = os.path.join(base_path, 'test_files')
    file_paths = get_file_paths(base_path, file_types)

    # check repo urls
    checker = UrlChecker(print_all=print_all)
    check_results = checker.run(
        file_paths=file_paths,
        white_listed_urls=white_listed_urls,
        white_listed_patterns=white_listed_patterns,
        retry_count=retry_count,
        timeout=timeout,
    )

    # Test saving to file
    output_file = os.path.join(str(tmp_path), 'results.csv')
    assert(not os.path.exists(output_file))
    saved_file = checker.save_results(output_file)
    assert(os.path.exists(output_file))

    # Read in output file
    with open(saved_file, 'r') as filey:
        lines = filey.readlines()

    # Header line has three items
    assert(lines[0] == 'URL,RESULT,FILENAME\n')

    # Ensure content looks okay
    for line in lines[1:]:
        url, result, filename = line.split(',')
        assert(url.startswith('http'))
        assert(result in ['passed', 'failed'])
        assert(re.search('(.py|.md)$', filename))


@pytest.mark.parametrize("save", [True])
def test_save(save):

    # init config parser
    config = configparser.ConfigParser()
    config.read("./tests/_local_test_config.conf")

    # init env variables
    path = config["DEFAULT"]["git_path_test_value"]
    file_types = config["DEFAULT"]["file_types_test_values"]
    white_listed_urls = config["DEFAULT"]["white_listed_test_urls"]
    white_listed_patterns = config["DEFAULT"]["white_listed__test_patterns"]

    # Generate command
    cmd = [
        "urlchecker",
        "check",
        "--subfolder",
        "test_files",
        "--file-types",
        file_types,
        "--white-listed-files",
        "conf.py",
        "--white-listed-urls",
        white_listed_urls,
        "--white-listed_patterns",
        white_listed_patterns,
    ]

    # Write to file
    if save:
        output_csv = tempfile.NamedTemporaryFile(suffix=".csv", prefix="urlchecker-")
        cmd += ["--save", output_csv.name]

    # Add final path
    cmd.append(path)

    print(" ".join(cmd))
    # excute script
    pipe = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if save:
        if not os.path.exists(output_csv.name):
            raise AssertionError
