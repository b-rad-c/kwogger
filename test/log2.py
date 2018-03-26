#!/usr/bin/env python3
import Kwogger

logger = Kwogger.log('myapp.log', 'submodule')

logger.warn('I am a submodule!')

logger.info('Submodule stuff happening here')
