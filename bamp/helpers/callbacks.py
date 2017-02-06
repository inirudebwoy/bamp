import logging
import sys

import click

from bamp.config import find_config, make_default_map, prepare_config
from bamp.exc import ErrorConfigParsing
from bamp.logs import LOGGING

logger = logging.getLogger(__name__)


def required(ctx, param, value):
    """Make sure that option passed in has value

    Some options can be passed from the command line, using flags, like
    --version or be retrieved from config file. Function makes sure
    that passed option has a value.

    """
    if not value:
        raise click.UsageError(
            '"%(name)s" is required. Add to config or pass with %(flag)s '
            'option.' % {'name': param.name,
                         'flag': param.opts})
    return value


def read_config(ctx, param, value):
    """Load config file passed as an argument

    If no file path is passed default value is taken.

    """
    config_path = value or find_config()
    config = {}
    if config_path:

        try:
            config = prepare_config(config_path)
        except ErrorConfigParsing:
            logger.exception('Could not parse the config file.')
            sys.exit(1)

    ctx.default_map = make_default_map(config)
    return value


def enable_debug(ctx, param, value):
    """Enable debugging"""
    logging.config.dictConfig(LOGGING)
    if value:
        LOGGING['filters']['exc_filter']['debug'] = True
        logger.debug('Debug is on.')
        logging.config.dictConfig(LOGGING)

    return value
