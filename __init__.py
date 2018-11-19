import logging
import uuid
import time
import os
from dataclasses import dataclass

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


@dataclass
class KwoggerTimer:
    name: str
    start_time: int = time.time()
    end_time: int = 0

    def __post_init__(self):
        self.start_time = time.time()

    def elapsed_time(self):
        if self.end_time == 0:
                return time.time() - self.start_time
        else:
            return self.end_time - self.start_time

    def stop(self):
        self.end_time = time.time()

    def __iter__(self):
        yield 'timer_name', self.name
        yield 'start_time', self.start_time
        yield 'elapsed_time', self.elapsed_time()
        if self.end_time != 0:
            yield 'end_time', self.end_time


class KwogFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(KwogFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(KwogFormatter, self).format(record)
        # import pdb; pdb.set_trace()
        try:
            for key, value in record.args['entry'].items():
                s += f'e.{key}={value} '

            for key, value in record.args['global_'].items():
                s += f'g.{key}={value} '
        except Exception:
            pass

        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


class KwoggerAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def __init__(self, logger, global_):
        """
        Initialize the adapter with a logger and a dict-like object which
        provides contextual information. This constructor signature allows
        easy stacking of LoggerAdapters, if so desired.
        You can effectively pass keyword arguments as shown in the
        following example:
        adapter = LoggerAdapter(someLogger, dict(p1=v1, p2="v2"))
        """
        self.logger = logger
        self.global_ = global_
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
            self.logger.log(level, msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        self.log(DEBUG, msg, *args, **kwargs)
    
    def debug_exc(self, msg, *args, **kwargs):
        self.log(DEBUG, msg, *args, exc_info=True, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        self.log(INFO, msg, *args, **kwargs)
    
    def info_exc(self, msg, *args, **kwargs):
        self.log(INFO, msg, *args, exc_info=True, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        self.log(WARNING, msg, *args, **kwargs)
    
    def warning_exc(self, msg, *args, **kwargs):
        self.log(WARNING, msg, *args, exc_info=True, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        self.log(ERROR, msg, *args, **kwargs)
    
    def error_exc(self, msg, *args, **kwargs):
        self.log(ERROR, msg, *args, exc_info=True, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(CRITICAL, msg, *args, **kwargs)

    def critical_exc(self, msg, *args, **kwargs):
        self.log(CRITICAL, msg, *args, exc_info=True, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.log(ERROR, msg, *args, exc_info=True, **kwargs)

    def timer_start(self, name, **kwargs):
        self.timers[name] = KwoggerTimer(name)
        kwargs.update(dict(self.timers[name]))
        self.log(INFO, 'TIMER_STARTED', **kwargs)

    def timer_stop(self, name, **kwargs):
        try:
            self.timers[name].stop()
        except KeyError:
            raise ValueError(f'No timer named: {name}')
        kwargs.update(dict(self.timers[name]))
        self.log(INFO, 'TIMER_STOPPED', **kwargs)

    def timer_checkpoint(self, name, **kwargs):
        try:
            kwargs.update(dict(self.timers[name]))
        except KeyError:
            raise ValueError(f'No timer named: {name}')
        self.log(INFO, 'TIMER_CHECKPOINT', **kwargs)


def configure(log_file='logs/example.log'):
    fh = logging.FileHandler(log_file, 'w')
    f = KwogFormatter('%(asctime)s | %(levelname)s | %(message)s | ', '%d/%m/%Y %H:%M:%S')
    fh.setFormatter(f)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(fh)
