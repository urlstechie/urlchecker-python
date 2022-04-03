import os
import sys
import pytest
import argparse
import tempfile
import subprocess
import configparser
from urlchecker.client import main as init_main
from urlchecker.client.check import main as check_main


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_all", [False])
@pytest.mark.parametrize("verbose", [True])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1])
@pytest.mark.parametrize("timeout", [3])
def test_client_init_(
    config_fname, cleanup, print_all, verbose, force_pass, rcount, timeout
):

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
        "--branch",
        "main",
        "--subfolder",
        "test_files",
        "--file-types",
        file_types,
        "--exclude-files",
        "conf.py",
        "--exclude-urls",
        exclude_urls,
        "--exclude-patterns",
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
    if verbose:
        cmd.append("--verbose")

    # Add final path
    cmd.append(path)

    # assign args and run main
    sys.argv = cmd
    with pytest.raises(SystemExit):
        init_main()


@pytest.mark.parametrize(
    "command", ["", "--version", "--help", "--unsupported_command"]
)
def test_command(command):
    # assign args and run main
    sys.argv = ["urlchecker", command]
    with pytest.raises(SystemExit):
        init_main()


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("no_print", [True])
@pytest.mark.parametrize("verbose", [False])
@pytest.mark.parametrize("force_pass", [False])
@pytest.mark.parametrize("rcount", [1])
@pytest.mark.parametrize("timeout", [3])
def test_arguments_from_cli(
    config_fname, cleanup, no_print, verbose, force_pass, rcount, timeout
):

    # init config parser
    config = configparser.ConfigParser()
    config.read("./tests/_local_test_config.conf")

    # Generate command
    cmd = argparse.Namespace(
        path=config["DEFAULT"]["git_path_test_value"],
        subfolder="test_files",
        branch="main",
        cleanup=str(cleanup),
        file_types=config["DEFAULT"]["file_types_test_values"],
        files="",
        no_print=str(no_print),
        exclude_urls=config["DEFAULT"]["exclude_test_urls"],
        exclude_patterns=config["DEFAULT"]["exclude_test_patterns"],
        exclude_files="conf.py",
        force_pass=str(force_pass),
        retry_count=rcount,
        save=None,
        timeout=timeout,
        verbose=verbose,
    )
    with pytest.raises(SystemExit):
        check_main(cmd, None)


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_all", [False, True])
@pytest.mark.parametrize("verbose", [False, True])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1, 3])
@pytest.mark.parametrize("timeout", [3, 5])
def test_client_general(
    config_fname, cleanup, print_all, verbose, force_pass, rcount, timeout
):

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
    if verbose:
        cmd.append("--verbose")

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
