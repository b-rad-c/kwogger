#!/usr/bin/env python3
import kwogger


def main():
    kwogger.rotate_by_size(__name__, level=kwogger.WARNING)
    logger = kwogger.log(__name__)

    logger.debug('This message should NOT go to the log file', key1='hello', key2='world', key3=1)

    logger.info('This message should NOT go to the log file')

    logger.warning('log me !')

    logger.error('Oh snap!', a=None, b=True, c=1, d=1.1, e='string', f=main)

    logger.critical('houston we have a problem!')


if __name__ == '__main__':
    main()
