#!/usr/bin/env python3
import kwogger
from random import randint


def main():
    kwogger.configure(__name__)
    logger = kwogger.log(__name__, connid=randint(1000, 9999))
    logger.generate_id(field='req_id')

    noise = '1' * 250
    print('Infinite loop to fill up log file and test automated rotation, press Ctrl+C to exit.')
    while True:
        logger.info('FILLING_LOG_FILE', noise=noise)


if __name__ == '__main__':
    main()
