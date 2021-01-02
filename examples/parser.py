#!/usr/bin/env python3
import kwogger

LOG_FILE = './parse.log'


def generate_log():
    log = kwogger.configure('parse-sample', LOG_FILE, kwogger.DEBUG)

    # basic
    log.debug("hmm... this doesn't look right")

    log.info('logging user info', color='orange', num=10)
    log.info('logging user info', color='blue', num=5)

    log.warning('Sample message', num=10)

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        log.error_exc('Problem dividing', x=x, y=y)


def parse():
    with kwogger.KwogFile(LOG_FILE) as log:
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

