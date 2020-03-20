"""
client/github.py: entrypoint for interaction with a GitHub repostiory.
Copyright (c) 2020 Ayoub Malek and Vanessa Sochat
"""





    # read input variables
    git_path = os.getenv("INPUT_GIT_PATH", "")
    branch = get_branch()
    subfolder = os.getenv("INPUT_SUBFOLDER", "")
    cleanup = os.getenv("INPUT_CLEANUP", "false").lower()
    file_types = os.getenv("INPUT_FILE_TYPES", "").split(",")
    print_all = os.getenv("INPUT_PRINT_ALL", "").lower()
    white_listed_urls = urlproc.remove_empty(
        os.getenv("INPUT_WHITE_LISTED_URLS", "").split(",")
    )
    white_listed_patterns = urlproc.remove_empty(
        os.getenv("INPUT_WHITE_LISTED_PATTERNS", "").split(",")
    )
    white_listed_files = urlproc.remove_empty(
        os.getenv("INPUT_WHITE_LISTED_FILES", "").split(",")
    )
    force_pass = os.getenv("INPUT_FORCE_PASS", "false").lower()
    retry_count = int(os.getenv("INPUT_RETRY_COUNT", 1))
    timeout = int(os.getenv("INPUT_TIMEOUT", 5))  # seconds

    # clone project repo if defined
    base_path = os.environ.get("GITHUB_WORKSPACE", os.getcwd())

    # Alert user about settings
    print("      base path: %s" % base_path)
    print("       git path: %s" % git_path)
    print("      subfolder: %s" % subfolder)
    print("         branch: %s" % branch)
    print("        cleanup: %s" % cleanup)
    print("     file types: %s" % file_types)
    print("      print all: %s" % print_all)
    print(" url whitetlist: %s" % white_listed_urls)
    print("   url patterns: %s" % white_listed_patterns)
    print("  file patterns: %s" % white_listed_files)
    print("     force pass: %s" % force_pass)
    print("    retry count: %s" % retry_count)
    print("        timeout: %s" % timeout)

    # If a custom base path is provided, clone and use it
    if git_path not in ["", None]:
        base_path = clone_repo(git_path, branch)

    if subfolder not in ["", None]:
        base_path = os.path.join(base_path, subfolder)

    # Assert that the base path exists
    if not os.path.exists(base_path):
        sys.exit("Cannot find %s to check" % base_path)

    # get all file paths
    file_paths = fileproc.get_file_paths(
        base_path=base_path,
        file_types=file_types,
        white_listed_files=white_listed_files,
    )

    # check repo urls
    check_results = check_repo(
        file_paths=file_paths,
        print_all=print_all,
        white_listed_urls=white_listed_urls,
        white_listed_patterns=white_listed_patterns,
        retry_count=retry_count,
        timeout=timeout,
    )

    # delete repo when done, if requested
    if cleanup == "true":
        del_repo(base_path)

    # exit
    if len(check_results) == 0:
        print("\n\nDone. No links were collected.")
        sys.exit(0)

    elif force_pass == "false" and len(check_results[1]) > 0:
        print("\n\nDone. The following URLS did not pass:")
        for failed_url in check_results[1]:
            print("\x1b[31m" + failed_url + "\x1b[0m")
        sys.exit(1)

    else:
        print("Done. All URLS passed.")
        sys.exit(0)
