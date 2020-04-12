import os
import pytest
from urlchecker.main.github import clone_repo, delete_repo, get_branch

@pytest.mark.parametrize(
    "git_path", ["https://github.com/urlstechie/urlchecker-test-repo"]
)
def test_clone_and_del_repo(git_path):
    """
    test clone and del repo function.
    """
    # del repo if it exisits
    if os.path.exists(os.path.basename(git_path)):
        delete_repo(os.path.basename(git_path))

    # clone
    repo_path = clone_repo(git_path)
    assert(os.path.exists(repo_path))
    assert(os.path.basename(repo_path).startswith(os.path.basename(git_path)))

    # delete should have return code of 0 (success)
    if not delete_repo(repo_path) == 0:
        raise AssertionError


def test_get_branch():
    """
    test getting branch from environment or default
    """
    # Unset defaults to master
    branch = get_branch()
    if branch != "master":
        raise AssertionError

    # Set both GitHub input variable and ref (ref takes priority)
    for pair in [["INPUT_BRANCH", "devel"], ["GITHUB_REF", "refs/heads/branchy"]]:
        os.environ[pair[0]] = pair[1]
        os.putenv(pair[0], pair[1])

    # Second preference should be for INPUT_BRANCH
    branch = get_branch()
    if branch != "devel":
        raise AssertionError

    del os.environ["INPUT_BRANCH"]
    os.unsetenv("INPUT_BRANCH")
    branch = get_branch()
    if branch != "branchy":
        raise AssertionError
