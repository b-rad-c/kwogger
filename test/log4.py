#!/usr/bin/env python3
import Kwogger

logger = Kwogger.log('myapp.log', 'fourthmodule')

logger.warn('I am a submodule!')

logger.info('THIS_MSG', a=None, b="hello "" world", c=True, x=1, y=-1, z=100.5)
