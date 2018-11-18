#!/usr/bin/env python3
import logging
import Kwogger
from random import randint


def main():
    Kwogger.configure()
    logger = Kwogger.KwoggerAdapter(logging.getLogger(__name__), dict(connid=str(randint(1000, 9999))))

    logging.debug('This message should go to the log file')
    logger.debug('This message should go to the log file')

    logging.info('So should this')
    logger.info('So should this')

    logging.warning('And this, too')
    logger.warning('And this, too')

    try:
        1 / 0
    except ZeroDivisionError:
        logger.debug_exc('do not do this!')
        logger.info_exc('do not do this!')
        logger.warning_exc('do not do this!')
        logger.error_exc('do not do this!')
        logger.exception('bad stuff happened!')


if __name__ == '__main__':
    main()
