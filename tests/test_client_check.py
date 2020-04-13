import os
import pytest
import subprocess
import tempfile
import configparser


@pytest.mark.parametrize("config_fname", ["./tests/_local_test_config.conf"])
@pytest.mark.parametrize("cleanup", [False, True])
@pytest.mark.parametrize("print_level", ["all", "only_files_with_urls", "fails-only", "success-only", "none"])
@pytest.mark.parametrize("force_pass", [False, True])
@pytest.mark.parametrize("rcount", [1, 3])
@pytest.mark.parametrize("timeout", [3, 5])
def test_client_general(config_fname, cleanup, print_level, force_pass, rcount, timeout):

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
        "--print_level",
        print_level,
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
