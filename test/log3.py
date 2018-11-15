#!/usr/bin/env python3
import Kwogger
import uuid
import datetime


def do_something(arg):
    logger.info('DOING_SOMETHING', arg=arg)


logger = Kwogger.log('myapp.log', 'kwargs', uuid=uuid.uuid1())

logger.debug('CHECK_ORDER_A', a=1, b=2, c=3, d=4, e=5, f=6)

logger.debug('CHECK_ORDER_A', a=1, b=2, f=6, c=3, d=4, e=5)

logger.debug('CHECK_ORDER_A', d=4, e=5, f=6, a=1, b=2, c=3)

logger.info('PROCESS_A_START', foo='ABC', baz='DEF', bar='GHI')

logger.warning('WARNING_TYPE_A', x=1, y=2)

try:
    int('a')

except ValueError:
    logger.error('INTEGER_ERROR', exc_info=True, color='GREEN', place='OREGON', number=7)

do_something(100)

logger.info('TEST_TYPES', a=None, b=True, c=1, d=1.5, e=datetime.datetime.now())

logger.info('TEST_ESCAPING', value1='LOOK AT THIS ,', value2='LOOK AT THAT "', value3='AND " THIS, THING',
            value4='AND "" THIS, THING', value5='AND """ THIS, THING')

if True:
    logger.info('TESTING_LIST', information=[
        None,
        True,
        1,
        2,
        'string',
        datetime.datetime.now(),
        {'x': True, 'y': 3, 'z': 'abc', 'zz': datetime.datetime.now()}
    ])

    logger.info('TESTING_DICT', stuff={
        'a': None,
        'b': True,
        'c': 2,
        'd': 'string',
        'e': datetime.datetime.now(),
        'f': [None, 1, 'abc', datetime.datetime.now()],
        'g': {'x': True, 'y': 3, 'z': 'abc', 'zz': datetime.datetime.now()}
    })
