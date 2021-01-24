#!/usr/bin/env python3
import kwogger


def main():
    main_log = kwogger.rotate_by_size('multi', 'multi.log', main_context=True)
    main_log.info('MESSAGE_1')

    log = kwogger.new('multi', 'request_id', main_log, first_request=True)
    log.info('MESSAGE_2')

    log = kwogger.new('multi', 'request_id', main_log, second_request=True)
    log.info('MESSAGE_3')


if __name__ == '__main__':
    main()
