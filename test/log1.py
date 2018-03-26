#!/usr/bin/env python3
import Kwogger

logger = Kwogger.log('myapp.log', 'myapp')

logger.info('Here is a message!')

logger.debug('Just so you know...')
