#!/usr/bin/env python3
import kwogger
import time


def main():
    log = kwogger.rotate_by_size('timer', 'timer.log')

    log.timer_start('hello', details='we are starting a timer named hello')

    time.sleep(1.5)

    log.timer_checkpoint('hello', details='we are logging a checkpoint for timer hello')
    
    time.sleep(1.5)

    log.timer_stop('hello', details='we are stopping the timer and logging the elapsed time')


if __name__ == '__main__':
    main()
