#!/usr/bin/env python3
import kwogger

LOG_FILE = './parse.log'


def generate():
    log = kwogger.rotate_by_size('parser', LOG_FILE)

    # basic
    log.debug("hmm... this doesn't look right")

    log.info('logging user info', color='orange', num=10)
    log.info('logging user info', color='blue', num=5)

    log.warning('Sample message', num=10)

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        log.error_exc('Problem dividing', x=x, y=y)


def display():
    with kwogger.KwogFile(LOG_FILE) as log:
        for entry in log:
            print(entry)


def parse():
    with kwogger.KwogFile(LOG_FILE) as log:
        for entry in log:
            print(repr(entry))
            print('\tsource   ', entry.source)
            print('\tentry    ', entry.entry)
            print('\tcontext  ', entry.context)
            print('\texception', entry.exc, '\n')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['generate', 'display', 'parse'])
    args = parser.parse_args()

    if args.mode == 'generate':
        generate()
    elif args.mode == 'display':
        display()
    elif args.mode == 'parse':
        parse()

