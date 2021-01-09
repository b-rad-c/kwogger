#!/usr/bin/env python3
import kwogger


def main():
    # shortcut to instantiate a KwogAdapter that rotates files by size
    log = kwogger.rotate_by_size('simple', 'simple.log', hello='world', global_context_data=True)

    # this and subsequent calls will also log kwargs from instantiation (hello='world', global_context_data=True)
    log.info('Sample message')

    # add data for just this log call with additional kwargs
    log.info('Sample message', key1='hello', key2='world')

    # built in parser can retain these data types, all others are converted to str before logging
    log.info('Sample message', a=None, b=True, c=1, d=1.1, e='string')

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        log.error_exc('Problem dividing', x=x, y=y)


if __name__ == '__main__':
    main()
