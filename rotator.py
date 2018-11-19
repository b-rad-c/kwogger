#!/usr/bin/env python3
import logging
import Kwogger
from random import randint


def main():
    Kwogger.configure()
    logger = Kwogger.KwogAdapter(logging.getLogger(__name__), dict(connid=randint(1000, 9999)))
    logger.generate_id(field='req_id')

    noise = '1' * 250
    while True:
        logger.info('FILLING_LOG_FILE', noise=noise)


if __name__ == '__main__':
    main()
