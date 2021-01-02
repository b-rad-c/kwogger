#!/usr/bin/env python3
import kwogger
import time


def main():
    kwogger.rotate_by_size(__name__)
    logger = kwogger.log(__name__)

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
