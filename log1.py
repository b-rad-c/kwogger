#!/usr/bin/env python3
import logging


logging.basicConfig(filename='logs/example.log', level=logging.DEBUG)
logger = logging.getLogger('log1')

logging.debug('This message should go to the log file')
logger.debug('This message should go to the log file')

logging.info('So should this')
logger.info('So should this')

logging.warning('And this, too')
logger.warning('And this, too')

try:
    'a' + 0
except TypeError:
    logging.exception('this is bad match')
    logger.exception('this is bad match')
