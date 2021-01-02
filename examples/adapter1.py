#!/usr/bin/env python3
import kwogger


def main():
    kwogger.rotate_by_size(__name__)
    logger = kwogger.log(__name__, namespace='test-value')

    id_ = logger.generate_id(field='req_id')
    print('got an id', id_)

    logger.log(kwogger.INFO, 'dynamic log entry', a=101)

    logger.debug('This message should go to the log file', key1='hello', key2='world', key3=1)

    logger.info('So should this')

    logger.global_['new_value'] = True

    logger.warning('And this, too')

    logger.error('Oh snap!', a=None, b=True, c=1, d=1.1, e='string', f=main)

    logger.critical('houston we have a problem')

    try:
        1 / 0
    except ZeroDivisionError:
        logger.log_exc(kwogger.INFO, 'do not do this!!!')
        logger.debug_exc('do not do this!')
        logger.info_exc('do not do this!')
        logger.warning_exc('do not do this!')
        logger.error_exc('do not do this!', a=1)
        logger.critical_exc('are you serious?')
        logger.exception('bad stuff happened!', b=2)


if __name__ == '__main__':
    main()
