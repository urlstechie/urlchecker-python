import os
import pytest
import argparse
import tempfile
import subprocess
import configparser
from urlchecker.client import check


def test_client_general():
    # excute scripts
    pipe = subprocess.run(
        ["urlchecker", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert pipe.stderr.decode("utf-8") == ""

    pipe = subprocess.run(
        ["urlchecker", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert pipe.stderr.decode("utf-8") == ""

    pipe = subprocess.run(
        ["urlchecker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert pipe.stderr.decode("utf-8") == ""


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_all", [False, True])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1, 3])
@pytest.mark.parametrize("timeout", [5, 7])
def test_client_check(config_fname, cleanup, print_all, force_pass, rcount, timeout):

    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # init env variables
    path = config["DEFAULT"]["git_path_test_value"]
    file_types = config["DEFAULT"]["file_types_test_values"]
    exclude_urls = config["DEFAULT"]["exclude_test_urls"]
    exclude_patterns = config["DEFAULT"]["exclude_test_patterns"]

    # Generate command
    cmd = [
        "urlchecker",
        "check",
        "--subfolder",
        "test_files",
        "--file-types",
        file_types,
        "--exclude-files",
        "conf.py",
        "--exclude-urls",
        exclude_urls,
        "--exclude_patterns",
        exclude_patterns,
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


@pytest.mark.parametrize("save", [True])
def test_client_save(save):

    # init config parser
    config = configparser.ConfigParser()
    config.read("./tests/_local_test_config.conf")

    # init env variables
    path = config["DEFAULT"]["git_path_test_value"]
    file_types = config["DEFAULT"]["file_types_test_values"]
    exclude_urls = config["DEFAULT"]["exclude_test_urls"]
    exclude_patterns = config["DEFAULT"]["exclude_test_patterns"]

    # Generate command
    cmd = [
        "urlchecker",
        "check",
        "--subfolder",
        "test_files",
        "--file-types",
        file_types,
        "--exclude-files",
        "conf.py",
        "--exclude-urls",
        exclude_urls,
        "--exclude_patterns",
        exclude_patterns,
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


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
def test_client_check_main(config_fname):

    # init config parser
    config = configparser.ConfigParser()
    config.read(config_fname)

    # init env variables
    path = config["DEFAULT"]["git_path_test_value"]
    file_types = config["DEFAULT"]["file_types_test_values"]
    exclude_urls = config["DEFAULT"]["exclude_test_urls"]
    exclude_patterns = config["DEFAULT"]["exclude_test_patterns"]

    # init args
    args = argparse.Namespace()
    args.path = path
    args.branch = "master"
    args.subfolder = "test_files"
    args.cleanup = True
    args.force_pass = True
    args.no_print = True
    args.file_types = file_types
    args.files = ""
    args.exclude_urls = ""
    args.exclude_patterns = ""
    args.exclude_files = ""
    args.save = ""
    args.retry_count = 1
    args.timeout = 5

    # excute script
    with pytest.raises(SystemExit) as e:
        check.main(args=args, extra=[])
    assert e.value.code == 0
