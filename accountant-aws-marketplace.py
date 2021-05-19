#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# accountant-aws-marketplace.py
# -----------------------------------------------------------------------------

import boto3
from datetime import datetime
import logging
import os
import requests
import sys

__all__ = []
__version__ = "1.0.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2021-05-17'
__updated__ = '2021-05-19'

SENZING_PRODUCT_ID = "5021"  # See https://github.com/Senzing/knowledge-base/blob/master/lists/senzing-product-ids.md
log_format = '%(asctime)s %(message)s'

# Docker HEALTHCHECK values.

OK = 0
NOT_OK = 1


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
    #  - account()
    #  - close()
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *args,
        **kwargs
    ):

        self.client = boto3.client('meteringmarketplace')

        # Context variables priority:  1) kwargs for account(); 2) kwargs for init(); 3) OS environment variables.

        self.dry_run = False
        dry_run_value = kwargs.get('dry_run', os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_DRY_RUN", False))
        if dry_run_value:
            if isinstance(dry_run_value, bool):
                self.dry_run = dry_run_value
            elif isinstance(dry_run_value, str):
                if dry_run_value.lower() in ['true', '1', 't', 'y', 'yes']:
                    self.dry_run = True

        self.product_code = kwargs.get('product_code', os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_PRODUCT_CODE", "000000"))
        self.usage_dimension = kwargs.get('usage_dimension', os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_USAGE_DIMENSION", "generic"))
        self.usage_quantity = int(kwargs.get('usage_quantity', os.getenv("SENZING_ACCOUNTANT_AWS_MARKETPLACE_USAGE_QUANTITY", 1)))

    def account(self, *args, **kwargs):
        """ Do the actual "accounting". """

        # Calculate context variables.

        dry_run = kwargs.get("dry_run", self.dry_run)
        product_code = kwargs.get("product_code", self.product_code)
        timestamp = datetime.now()
        usage_dimension = kwargs.get("usage_dimension", self.usage_dimension)
        usage_quantity = kwargs.get("usage_quantity", self.usage_quantity)

        # Make HTTP request to AWS to register metering.

        try:
            response = self.client.meter_usage(
                DryRun=dry_run,
                ProductCode=product_code,
                Timestamp=timestamp,
                UsageDimension=usage_dimension,
                UsageQuantity=usage_quantity
            )
            logging.info("senzing-{0}0002I Accounting Response: {1}".format(SENZING_PRODUCT_ID, response))

        except Exception as err:
            logging.error("senzing-{0}0701E Error: {1}".format(SENZING_PRODUCT_ID, err))
            sys.exit(NOT_OK)

    def close(self, *args, **kwargs):
        """  Tasks to perform when shutting down. """

        pass

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


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

    # FIXME:  Temporary test to verify Accountant has been invoked.

    response = requests.get('http://michael.dockter.com')

    # Create accountant.

    with Accountant() as accountant:
        accountant.account()

    # Epilog.

    sys.exit(OK)
