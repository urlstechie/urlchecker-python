"""

Copyright (c) 2020 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import sys
import subprocess
from urlchecker.core import urlproc
from urlchecker.core import fileproc


def clone_repo(git_path, branch="master"):
    """
    Clone and name a git repository.

    Args:
        - git_path (str) : https path to git repository.
        - branch   (str) : name of the brankch to use. Default="master"

    Returns:
        (str) base path of the cloned git repository.
    """
    base_path = os.path.basename(git_path)
    result = subprocess.run(
        ["git", "clone", "-b", branch, git_path, base_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        sys.exit("Issue with cloning branch %s of %s" % (branch, git_path))

    return base_path


def delete_repo(base_path):
    """
    Delete repository.

    Args:
        - base_path (str) : base path of the cloned git repository.

    Returns:
        (str) message/ code describing whether the operation was successfully excuted.
    """
    # clone repo
    result = subprocess.run(
        ["rm", "-R", "-f", base_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.returncode



def get_branch(default="master"):
    """
    Derive the selected branch. We first look to the environment variable
    for INPUT_BRANCH, meaning that the user set the branch variable. If
    that is unset we parse GITHUB_REF. If both of those are unset,
    then we default to default (master).

    Returns:
        (str) the branch found in the environment, otherwise master.
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
