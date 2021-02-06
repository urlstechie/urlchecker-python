import os
import pytest
import subprocess
import tempfile
import configparser


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_all", [False, True])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1, 3])
@pytest.mark.parametrize("timeout", [3, 5])
def test_client_general(config_fname, cleanup, print_all, force_pass, rcount, timeout):

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
