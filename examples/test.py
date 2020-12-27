#!/usr/bin/env python3
import kwogger

LOG_FILE = './test.log'

kwogger.configure('parse-sample', LOG_FILE, kwogger.DEBUG)
logger = kwogger.log('parse-sample')

logger.info('HELLO.WORLD')
handler = logger.logger.handlers[0].close()

breakpoint()
