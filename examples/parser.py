#!/usr/bin/env python3
import kwogger
from kwogger.core import KwogFileIO

LOG_FILE = './parse.log'


def generate_log():
    kwogger.configure('parse-sample', LOG_FILE, kwogger.DEBUG)
    logger = kwogger.log('parse-sample')

    # basic
    logger.debug("hmm... this doesn't look right")

    logger.info('logging user info', color='orange', num=10)
    logger.info('logging user info', color='blue', num=5)

    logger.warning('Sample message', num=10)

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        logger.error_exc('Problem dividing', x=x, y=y)


def parse():
    with KwogFileIO(LOG_FILE) as log:
        for entry in log:
            breakpoint()
            print(type(entry))
            print(entry)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['generate_log', 'parse'])
    args = parser.parse_args()

    if args.mode == 'generate_log':
        generate_log()
    elif args.mode == 'parse':
        parse()

