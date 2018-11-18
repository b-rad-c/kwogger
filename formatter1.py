#!/usr/bin/env python3
import logging
import Kwogger


def main():
    Kwogger.configure()
    logging.info('Sample message')
    try:
        1 / 0
    except ZeroDivisionError as e:
        logging.exception('ZeroDivisionError: %s', e)


if __name__ == '__main__':
    main()
