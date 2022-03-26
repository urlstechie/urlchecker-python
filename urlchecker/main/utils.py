"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import os
import tempfile


def get_tmpdir(base_dir=None, prefix="", create=True):
    """get a temporary directory for an operation. If SREGISTRY_TMPDIR
    is set, return that. Otherwise, return the output of tempfile.mkdtemp


    Args:
        - base_dir (str)  : an optional requested base directory
        - prefix   (str)  : a prefix for the temporary directory
        - create:  (bool) : boolean if we should create dir (True)

    Returns:
       (str) full path to directory
    """
    tmpdir = base_dir or tempfile.gettempdir()
    prefix = prefix or "urlchecker-"
    prefix = "%s.%s" % (prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create is True:
        os.mkdir(tmpdir)

    return tmpdir
