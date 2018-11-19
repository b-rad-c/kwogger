#!/usr/bin/env python3
import logging
import Kwogger
from random import randint
import time


def main():
    Kwogger.configure()
    logger = Kwogger.KwoggerAdapter(logging.getLogger(__name__), dict(connid=str(randint(1000, 9999))))

    logger.timer_start('hello', value=1)

    try:
        logger.timer_checkpoint('bad_timer')
    except ValueError:
        logger.error_exc('bad_timer')

    try:
        logger.timer_stop('bad_timer')
    except ValueError:
        logger.error_exc('another_timer')

    time.sleep(1.5)

    logger.timer_checkpoint('hello', processing=True
                            )
    time.sleep(1.5)

    logger.timer_stop('hello', complete=True)


if __name__ == '__main__':
    main()
