import logging
from logging import Formatter, Logger
import datetime
from collections import OrderedDict
from Kwogger.core import KwogEntry


class Kwogger(Logger):
    DBG = False

    def _log(self, level, msg, args, exc_info=None, stack_info=True, **kwargs):
        super()._log(level, msg, args, exc_info, extra={'params': kwargs}, stack_info=stack_info)


logging.setLoggerClass(Kwogger)


class KwoggerFormatter(Formatter):

    def __init__(self, name=None, **_global):
        self.name = name
        self._global = _global

        super().__init__()

    def format(self, record):
        if Kwogger.DBG:
            import pdb; pdb.set_trace()

        # rewrite as literal, leave like this for quick testing OrderedDict
        source = OrderedDict()
        source['time'] = datetime.datetime.now()
        source['log'] = self.name
        source['level'] = record.levelname
        source['path'] = record.pathname
        source['func'] = record.funcName
        source['lineno'] = record.lineno

        entry = OrderedDict()
        entry['msg'] = record.msg
        entry.update(record.params)

        if record.exc_info:
            exc = OrderedDict()
            exc['class'] = KwogEntry.escape_value(record.exc_info[0].__name__)
            exc['msg'] = KwogEntry.escape_value(str(record.exc_info[1]))
            exc['stack'] = KwogEntry.escape_value(self.formatStack(record.stack_info))\

        else:
            exc = None

        return str(KwogEntry(self._global, source, entry, exc))


# add levels from logging to this namespace
CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

_level_to_name = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

_name_to_level = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


def get_level(level):
    """this function will return a tuple of (int, str) representing the integer value of level, level may be
    the integer or string representation of the level"""

    try:
        level_int = _name_to_level[level]
        return level_int, level
    except KeyError:
        pass

    try:
        level_name = _level_to_name[level]
        return level, level_name

    except KeyError:
        raise KeyError(f'Level not found: {level}')


def get_level_color(level):
    level_int = get_level(level)[0]

    if level_int < INFO:
        return 'white'

    if level_int < WARNING:
        return 'green'

    if level_int < ERROR:
        return 'yellow'

    return 'red'


def log(log_file, name, **_global):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(KwoggerFormatter(name, **_global))
    logger.addHandler(handler)

    return logger
