#!/usr/bin/env python3
import Kwogger
import uuid

logger = Kwogger.log('myapp.log', 'submodule', uuid=uuid.uuid1())
Kwogger.Kwogger.DBG = False


def function_one():
    return function_two()


def function_two():
    return int('a')


try:
    function_one()

except ValueError:
    logger.error('INTEGER_ERROR', exc_info=True, color='GREEN', place='OREGON', number=7)
