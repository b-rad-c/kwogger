import logging
import logging.handlers
import uuid
import time
import os
import datetime
import traceback
from collections import OrderedDict
from Kwogger.core import KwogTimer, KwogEntry


CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
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
        level_nm = _level_to_name[level]
        return level, level_nm

    except KeyError:
        raise KeyError(f'Level not found: {level}')


def level_value(level):
    """Convenience function to return integer regardless of input
    :param level (int/str) return corresponding integer"""
    return get_level(level)[0]


def level_name(level):
    """Convenience function to return string regardless of input
    :param level (int/str) return corresponding level name as str"""
    return get_level(level)[1]


def get_level_color(level):
    level_int = get_level(level)[0]

    if level_int < INFO:
        return 'white'

    if level_int < WARNING:
        return 'green'

    if level_int < ERROR:
        return 'yellow'

    return 'red'


class KwogFormatter(logging.Formatter):

    def format(self, record):

        # rewrite as literal, leave like this for quick testing OrderedDict
        source = OrderedDict()
        source['time'] = datetime.datetime.fromtimestamp(record.created)
        source['log'] = record.module
        source['level'] = record.levelname
        source['path'] = record.pathname
        source['func'] = record.funcName
        source['lineno'] = record.lineno

        entry = OrderedDict()
        entry['msg'] = record.msg
        entry.update(record.args['entry'])

        if record.exc_info:
            exc = OrderedDict()
            exc['class'] = KwogEntry.escape_value(record.exc_info[0].__name__)
            exc['msg'] = KwogEntry.escape_value(str(record.exc_info[1]))
            exc['traceback'] = KwogEntry.format_value(traceback.format_tb(record.exc_info[2]))

        else:
            exc = None

        return str(KwogEntry(record.args['global_'], source, entry, exc))


class KwogAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def __init__(self, logger, global_=None):
        """
        Initialize the adapter with a logger and a dict-like object which
        provides contextual information. This constructor signature allows
        easy stacking of LoggerAdapters, if so desired.
        You can effectively pass keyword arguments as shown in the
        following example:
        adapter = LoggerAdapter(someLogger, dict(p1=v1, p2="v2"))
        """
        self.logger = logger
        self.global_ = {} if global_ is None else global_
        self.timers = {}

    def generate_id(self, **kwargs):
        namespace = kwargs.get('namespace', uuid.uuid4())
        field = kwargs.get('field', 'uuid')

        self.global_[field] = uuid.uuid3(namespace, f'{time.time()}-{os.getpid()}')
        return self.global_[field]

    def process(self, msg, args, kwargs):
        try:
            exc_info = kwargs['exc_info']
            del kwargs['exc_info']
        except KeyError:
            exc_info = None

        args = [{'global_': self.global_, 'entry': kwargs}]

        return msg, args, {'exc_info': exc_info}

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(level, msg, *args, **kwargs)

    def log_exc(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(level, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(NOTSET):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(NOTSET, msg, *args, **kwargs)

    def trace_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(NOTSET):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(NOTSET, msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(DEBUG, msg, *args, **kwargs)
    
    def debug_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(DEBUG, msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(INFO, msg, *args, **kwargs)
    
    def info_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(INFO, msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(WARNING, msg, *args, **kwargs)
    
    def warning_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(WARNING, msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(ERROR, msg, *args, **kwargs)
    
    def error_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(CRITICAL, msg, *args, **kwargs)

    def critical_exc(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            msg, args, kwargs = self.process(msg, args, kwargs)
            kwargs['exc_info'] = True
            self.logger._log(CRITICAL, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            msg, args, kwargs = self.process(msg, args, kwargs)
            self.logger._log(ERROR, msg, *args, **kwargs)

    def timer_start(self, name, **kwargs):
        self.timers[name] = KwogTimer(name)
        kwargs.update(dict(self.timers[name]))
        msg = 'TIMER_STARTED'
        msg, args, kwargs = self.process(msg, [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)

    def timer_stop(self, name, **kwargs):
        try:
            self.timers[name].stop()
        except KeyError:
            raise ValueError(f'No timer named: {name}')
        kwargs.update(dict(self.timers[name]))
        msg = 'TIMER_STOPPED'
        msg, args, kwargs = self.process(msg, [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)

    def timer_checkpoint(self, name, **kwargs):
        try:
            kwargs.update(dict(self.timers[name]))
        except KeyError:
            raise ValueError(f'No timer named: {name}')
        msg = 'TIMER_CHECKPOINT'
        msg, args, kwargs = self.process(msg, [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)


def configure(name, log_file='logs/example.log', level=logging.DEBUG):
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=5)    # 5 MB
    f = KwogFormatter()
    fh.setFormatter(f)
    root = logging.getLogger(name)
    root.setLevel(level)
    root.addHandler(fh)


def log(name, **global_):
    return KwogAdapter(logging.getLogger(name), global_)
