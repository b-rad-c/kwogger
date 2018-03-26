#!/usr/bin/env python3
import Kwogger
import uuid

logger = Kwogger.log('myapp.log', 'submodule', uuid=uuid.uuid1())
Kwogger.Kwogger.DBG = False

try:
    int('a')

except ValueError:
    logger.error('INTEGER_ERROR', exc_info=True, color='GREEN', place='OREGON', number=7)