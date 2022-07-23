"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import subprocess
import sys

from urlchecker.main.utils import get_tmpdir


def clone_repo(git_path: str, branch: str = "master", dest: str = None) -> str:
    """
    Clone and name a git repository.

    Args:
        - git_path (str) : https path to git repository.
        - branch   (str) : name of the branch to use. Default="master"
        - dest     (str) : fullpath to clone repository to. Defaults to tmp.

    Returns:
        (str) base path of the cloned git repository.
    """
    if not dest:
        base_path = os.path.basename(git_path)
        dest = get_tmpdir(prefix=base_path, create=False)

    result = subprocess.run(
        ["git", "clone", "-b", branch, git_path, dest],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        sys.exit("Issue with cloning branch %s of %s" % (branch, git_path))

    return dest


def delete_repo(base_path: str) -> int:
    """
    Delete repository.

    Args:
        - base_path (str) : base path of the cloned git repository.

    Returns:
        (int) Exit status of the child process.

    Remark:
        The exit status is typically, an exit status of 0 indicates that it ran successfully.
        A negative value -N indicates that the child was terminated by signal N (POSIX only)
    """
    # clone repo
    result = subprocess.run(
        ["rm", "-R", "-f", base_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.returncode


def get_branch(default: str = "main") -> str:
    """
    Derive the selected branch. We first look to the environment variable
    for INPUT_BRANCH, meaning that the user set the branch variable. If
    that is unset we parse GITHUB_REF. If both of those are unset,
    then we default to default (main).

    Returns:
        (str) the branch found in the environment, otherwise main.
    """
    # First check goes to use setting in action
    branch = os.getenv("INPUT_BRANCH")
    if branch:
        return branch

    # Second check is for GITHUB_REF
    branch = os.getenv("GITHUB_REF")
    if branch:
        branch = branch.replace("refs/heads/", "")
        return branch
    return default
