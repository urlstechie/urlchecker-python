"""

Copyright (c) 2020-2022 Ayoub Malek and Vanessa Sochat

This source code is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.

"""

import itertools
import multiprocessing
import os
import time
import signal
import sys

from urlchecker.logger import get_logger

logger = get_logger()


class Workers:
    def __init__(self, workers=None):

        if workers is None:
            workers = int(os.environ.get("URLCHECKER_WORKERS", 9))
        self.workers = workers
        logger.debug(f"Using {self.workers} workers for multiprocess.")

    def start(self):
        logger.debug("Starting multiprocess")
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.runtime = self.runtime = self.end_time - self.start_time
        logger.debug(f"Ending multiprocess, runtime: {self.runtime} sec")

    def run(self, funcs, tasks):
        """run will send a list of tasks, a tuple with arguments, through a function.
        the arguments should be ordered correctly.

        Parameters
        ==========
        funcs: the functions to run with multiprocessing.pool, a dictionary
               with lookup by the task name
        tasks: a dict of tasks, each task name (key) with a
               tuple of arguments to process
        """
        # Number of tasks must == number of functions
        assert len(funcs) == len(tasks)

        # Keep track of some progress for the user
        progress = 1

        # if we don't have tasks, don't run
        if not tasks:
            return

        # results will also have the same key to look up
        finished = dict()
        results = []

        try:
            pool = multiprocessing.Pool(self.workers, init_worker)

            self.start()
            for key, params in tasks.items():
                func = funcs[key]
                result = pool.apply_async(multi_wrapper, multi_package(func, [params]))

                # Store the key with the result
                results.append((key, result))

            while len(results) > 0:
                pair = results.pop()
                key, result = pair
                result.wait()
                progress += 1
                finished[key] = result.get()

            self.end()
            pool.close()
            pool.join()

        except (KeyboardInterrupt, SystemExit):
            logger.error("Keyboard interrupt detected, terminating workers!")
            pool.terminate()
            sys.exit(1)

        except:
            logger.exit("Error running task")

        return finished


# Supporting functions for MultiProcess Worker
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def multi_wrapper(func_args):
    function, kwargs = func_args
    return function(**kwargs)


def multi_package(func, kwargs):
    zipped = zip(itertools.repeat(func), kwargs)
    return zipped
