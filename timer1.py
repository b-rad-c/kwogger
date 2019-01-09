#!/usr/bin/env python3
import Kwogger
import time


def main():
    Kwogger.configure(__name__)
    logger = Kwogger.log(__name__)

    try:
        logger.timer_checkpoint('bad_timer')
    except ValueError:
        logger.error_exc('bad_timer')

    try:
        logger.timer_stop('bad_timer')
    except ValueError:
        logger.error_exc('another_timer')

    logger.timer_start('hello', value=1)

    time.sleep(1.5)

    logger.timer_checkpoint('hello', processing=True
                            )
    time.sleep(1.5)

    logger.timer_stop('hello', complete=True)


if __name__ == '__main__':
    main()
