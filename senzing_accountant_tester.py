#! /usr/bin/env python3

import logging
import time
import os
import threading

import senzing_accountant
from senzing_accountant import Accountant

__all__ = []
__version__ = "1.0.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2021-05-17'
__updated__ = '2021-05-18'

log_format = '%(asctime)s %(message)s'

# -----------------------------------------------------------------------------
# Class: ExampleThread
# -----------------------------------------------------------------------------


class ExampleThread(threading.Thread):

    def __init__(self, accountant, counter_max):
        threading.Thread.__init__(self)
        self.accountant = accountant

    def run(self):
        self.accountant.account()
        logging.info("{0}".format(threading.current_thread().name))

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------


if __name__ == '__main__':

    # Configure logging.

    log_level = logging.INFO
    logging.basicConfig(format=log_format, level=log_level)
    logging.info("Accountant file: {0}".format(senzing_accountant.__file__))

    # Create Accountant.

    accountant = Accountant(hint="Tester")

    # Create threads.

    threads = []
    for i in range(0, 5):
        thread = ExampleThread(accountant, 1000)
        thread.name = "{0}-thread-{1}".format(ExampleThread.__name__, i)
        threads.append(thread)

    # Start threads.

    for thread in threads:
        thread.start()

    # Collect inactive threads.

    for thread in threads:
        thread.join()

    # Done with Accountant.

    accountant.close()
