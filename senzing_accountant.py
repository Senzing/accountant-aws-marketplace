#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# senzing_accountant.py
#
# Class: Accountant
#
# --------------------------------------------------------------------------------------------------------------

import boto3
import json
import logging
from datetime import datetime
import os
import re
import string
import threading
import time

__all__ = []
__version__ = "1.0.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2021-05-17'
__updated__ = '2021-05-17'

SENZING_PRODUCT_ID = "5020"  # See https://github.com/Senzing/knowledge-base/blob/master/lists/senzing-product-ids.md
log_format = '%(asctime)s %(message)s'


class Accountant:

    # -------------------------------------------------------------------------
    # Support for Python Context Manager.
    # -------------------------------------------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    # -------------------------------------------------------------------------
    # Public API methods.
    #  - govern()
    #  - close()
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *args,
        **kwargs
    ):

        logging.info("senzing-{0}0001I Using accountant-aws-marketplace Accountant. Version: {1} Updated: {2}".format(SENZING_PRODUCT_ID, __version__, __updated__))
        self.client = boto3.client('meteringmarketplace')
        self.product_code = os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_PRODUCT_CODE", "not-submitted")
        self.dry_run = os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_DRY_RUN", False)


    def account(self, *args, **kwargs):
        """
        Do the actual "accounting".
        """

        timestamp = datetime.now()
        usage_dimension = "string"
        usage_allocations = [
            {
                'AllocatedUsageQuantity': 123,
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ]
            },
        ]
        usage_allocation = sum([x.get("AllocatedUsageQuantity") for x in usage_allocations])

        try:
            response = self.client.meter_usage(
                DryRun=self.dry_run,
                ProductCode=self.product_code,
                Timestamp=timestamp,
                UsageAllocations=usage_allocations,
                UsageDimension=usage_dimension,
                UsageQuantity=usage_quantity
            )
            logging.info("senzing-{0}0002I Response: {1}".format(SENZING_PRODUCT_ID, response))

        except Exception as err:
            pass


    def close(self, *args, **kwargs):
        '''  Tasks to perform when shutting down '''

        pass



if __name__ == '__main__':

    # Configure logging. See https://docs.python.org/2/library/logging.html#levels

    log_level_map = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "fatal": logging.FATAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    log_level_parameter = os.getenv("SENZING_LOG_LEVEL", "info").lower()
    log_level = log_level_map.get(log_level_parameter, logging.INFO)
    logging.basicConfig(format=log_format, level=log_level)

    # Create governor.

    accountant = Accountant()
