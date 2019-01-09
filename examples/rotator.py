#!/usr/bin/env python3
import Kwogger
from random import randint


def main():
    Kwogger.configure(__name__)
    logger = Kwogger.log(__name__, connid=randint(1000, 9999))
    logger.generate_id(field='req_id')

    noise = '1' * 250
    while True:
        logger.info('FILLING_LOG_FILE', noise=noise)


if __name__ == '__main__':
    main()
