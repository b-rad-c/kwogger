#!/usr/bin/env python3
import kwogger


def main():
    log = kwogger.rotate_by_size('request_demo', 'request_id.log', server='www.example.com')

    # create a unique id for this mock web request that links each logging entry for easy searching when troubleshooting
    log.generate_id('request_id')

    log.info('Sample message')

    x, y = 1, '1'
    try:
        z = x + y
    except TypeError:
        log.error_exc('Uh-oh!', x=x, y=y)


if __name__ == '__main__':
    main()
