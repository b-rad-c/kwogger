import logging
import logging.handlers
import uuid
import time
import os
import datetime
import traceback
from collections import OrderedDict
from termcolor import colored
from dataclasses import dataclass, field


#
# logging levels
#

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


def configure(name, log_file='logs/example.log', level=logging.DEBUG, **global_):
    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=5)
    f = KwogFormatter()
    fh.setFormatter(f)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)
    return KwogAdapter(logger, global_)


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

    def generate_id(self, field_name='uuid', namespace=None):
        _id = str(uuid.uuid3(uuid.uuid4() if namespace is None else namespace, f'{time.time()}-{os.getpid()}'))
        self.global_[field_name] = _id
        return _id

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
        del kwargs['elapsed_time']
        del kwargs['end_time']

        msg, args, kwargs = self.process('TIMER_STARTED', [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)

    def timer_stop(self, name, **kwargs):
        try:
            self.timers[name].stop()
            kwargs.update(dict(self.timers[name]))
        except KeyError:
            raise ValueError(f'No timer named: {name}')

        msg, args, kwargs = self.process('TIMER_STOPPED', [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)

    def timer_checkpoint(self, name, **kwargs):
        try:
            kwargs.update(dict(self.timers[name]))
            del kwargs['end_time']
        except KeyError:
            raise ValueError(f'No timer named: {name}')

        msg, args, kwargs = self.process('TIMER_CHECKPOINT', [], kwargs)
        self.logger._log(INFO, msg, *args, **kwargs)





#
#
#
#
#


class KeyExists:
    pass


@dataclass
class KwogTimer:
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: float = None

    def elapsed_time(self):
        try:
            return self.end_time - self.start_time
        except TypeError:
            return time.time() - self.start_time

    def stop(self):
        self.end_time = time.time()

    def __iter__(self):
        yield 'timer_name', self.name
        yield 'start_time', self.start_time
        yield 'elapsed_time', self.elapsed_time()
        if self.end_time != 0:
            yield 'end_time', self.end_time


class ParseError(Exception):
    def __init__(self, msg, parser=None):
        self.msg = msg
        self.parser = parser

    def __str__(self):
        return str(self.msg)


class Parser:

    DBG = True

    def __init__(self, line):
        self.line = line.strip()
        self.pairs = []
        self.log = []
        self.data = {}
        self.index = 0

        self.append_log('** initialized **')
        self.append_log(f'==={self.line}===')

        self.parse()

    def __str__(self):
        return str(self.data)

    def display_log(self):
        print('=' * 10 + ' BEGIN KWOGGER PARSER LOG ' + '=' * 10)
        for item in self.log:
            print(item)
        print('=' * 10 + ' END KWOGGER PARSER LOG ' + '=' * 10)

    def append_log(self, msg):
        """this log is used to debug parser"""
        self.log.append(msg)

    def parse(self):
        self._parse_pairs()
        self._format_pairs()

    def _parse_pairs(self):
        self.append_log('** _parse_pairs()')
        last_break = 0
        in_string = False
        escaping = False
        for index, char in enumerate(self.line):
            self.append_log(f'index: {index} char: {char}')

            if escaping and char in ['\n', ' ', '']:
                self.append_log(f'      > out of string (end of string)')
                escaping = False
                in_string = False
                self.pairs.append(self.line[last_break:index])
                last_break = index + 1

            elif escaping and char == '"':
                self.append_log(f'      > unescape')
                escaping = False

            elif escaping:
                self.append_log(f'      > unescape | out of string')
                escaping = False
                in_string = False

            elif char == ' ' and not in_string:
                self.append_log(f'      > a: {self.line[last_break:index]}')
                self.pairs.append(self.line[last_break:index])
                last_break = index + 1

            elif char == '"' and not in_string:
                self.append_log(f'      > in string')
                in_string = True

            elif char == '"' and in_string:
                self.append_log(f'      > escaping')
                escaping = True

        if escaping:
            in_string = False

        if in_string:
            raise ParseError('Could not find end of string', self)

        self.pairs.append(self.line[last_break:])

        self.append_log('** end _parse_pairs()')

        self.append_log('** pairs **')

        for pair in self.pairs:
            self.append_log(pair)

    def _format_pairs(self):
        self.append_log('** _format_pairs()')
        for pair in self.pairs:

            try:
                key, value = pair.split('=', 1)
            except ValueError:
                raise ParseError(f'Could not parse key/value from: "{pair}"', self)

            parsed_value = self._format_value(value)

            ns = key.split('.')

            if len(ns) == 1:
                self.data[key] = parsed_value

            if len(ns) == 2:
                try:
                    self.data[ns[0]][ns[1]] = parsed_value
                except KeyError:
                    self.data[ns[0]] = {ns[1]: parsed_value}

            self.append_log('** end _format_pairs()')

    def _format_value(self, value):
        self.append_log('** _format_value()')

        if value == '.':
            """used in searching logs, if this value is searched for all objects with any value this key
            will be returned"""
            self.append_log('  > value: KeyExists')
            return KeyExists

        if value == 'None':
            self.append_log('  > value: None')
            return None

        if value == 'True':
            self.append_log('  > value: True')
            return True

        if value == 'False':
            self.append_log('  > value: False')
            return False

        if str(value).find('.') != -1:
            try:
                float_value = float(value)
                self.append_log('  > value: float | {value}')
                return float_value
            except ValueError:
                pass

        try:
            int_value = int(value)
            self.append_log('  > value: int | {value}')
            return int_value
        except ValueError:
            pass

        if value[0:1] == '"' and value[-1:] == '"':
            self.append_log(f'  > value: str | len: {len(value)}')
            return value[1:-1].replace('""', '"')




            #
            #
            # original return
            #
            #



            # return value.replace('""', '"')

        self.append_log('  > value: default')
        return str(value)


class KwogFile:

    def __init__(self, path, level=DEBUG, seek='head'):
        self.path = path
        self.level = level
        self._file = open(path, 'r')

        if seek == 'head':
            self.seek_head()
        elif seek == 'tail':
            self.seek_tail()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            entry = self.parse_line()
            try:
                if entry.level >= self.level:
                    return entry
            except AttributeError:
                raise StopIteration

    #
    # file handler
    #

    def seek_head(self):
        self._file.seek(0)

    def seek_tail(self):
        self._file.seek(0, os.SEEK_END)

    def close(self):
        self._file.close()

    #
    # context manager
    #

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    #
    # methods for getting data
    #

    def follow(self):
        try:
            self.seek_tail()

            while True:
                line = self._file.readline()

                if line:
                    entry = KwogEntry.parse(line)
                    if entry.level >= self.level:
                        yield entry

        except KeyboardInterrupt:
            pass

    def parse_line(self):
        """parse the next line,
        formatter: method as formatter to use a specific formatter w/o changing self._format
        :returns: str, or None if we are at EOF"""
        line = self._file.readline()
        if line:
            return KwogEntry.parse(line)


class KwogEntry:

    def __init__(self, global_=None, source=None, entry=None, exc=None, raw=None):
        self.global_, self.source, self.entry, self.exc, self.raw,  = global_, source, entry, exc, raw

    def __str__(self):
        """line break between namespaces
        items = ' '.join(list(self.format_namespace('s', self.source))) + '\n'
        items += ' '.join(list(self.format_namespace('e', self.entry))) + '\n'
        if self.exc:
            items += ' '.join(list(self.format_namespace('exc', self.exc))) + '\n'
        items += ' '.join(list(self.format_namespace('g', self.global_))) + '\n'
        return items"""

        items = list(self.format_namespace('s', self.source))
        items.extend(list(self.format_namespace('e', self.entry)))
        if self.exc:
            items.extend(list(self.format_namespace('exc', self.exc)))

        items.extend(list(self.format_namespace('g', self.global_)))
        return ' '.join(items)

    def __iter__(self):
        for name, group in [('global', self.global_), ('source', self.source), ('entry', self.entry), ('exc', self.exc)]:
            try:
                for key, value in group.items():
                    yield '.'.join([name, key]), value
            except AttributeError:
                if group is KeyExists:
                    yield name, KeyExists

    @classmethod
    def parse(cls, line):
        p = Parser(line)
        return cls(p.data.get('g', {}), p.data.get('s', {}), p.data.get('e', {}), p.data.get('exc', {}), line)

    @staticmethod
    def escape_value(value):
        return value.replace('"', '""').replace('\n', '')

    @classmethod
    def format_value(cls, value):
        if value is None:
            return 'None'

        if isinstance(value, (bool, float, int)):
            return str(value)

        return '"' + cls.escape_value(str(value)) + '"'

    def format_namespace(self, parent, dictionary):
        for key, value in dictionary.items():

            # this is written to only go one level into lists/dicts, this is a logging library not a datastore
            # sub lists/dicts will be converted to a string

            yield '{}.{}={}'.format(parent, key, self.format_value(value))

    def format(self, formatter):
        try:
            _method = getattr(self, f'_formatter_{formatter}')

        except AttributeError:
            raise ValueError(f'No formatter named: {formatter}')

        try:
            return _method()
        except KeyError:
            print('***')
            print(str(self))
            print('***')
            raise

    #
    # formatters
    #

    def _formatter_raw(self):
        return self.raw

    def _formatter_data(self):
        return str(dict(self))

    def _formatter_basic(self):
        string = f'source: {self.source}\n'
        string += f'entry: {self.entry}\n'
        if self.exc != {}:
            string += f'exc: {self.exc}\n'
        if self.global_ != {}:
            string += f'global: {self.global_}\n'

        return string

    def _formatter_default(self):
        level = self.source["level"]

        #
        # format source line
        #

        string = f's: {self.source["time"]} {level} {self.source["log"]}'
        string += f' {self.string_trunc(self.source["path"])} func: {self.source["func"]} line: {self.source["lineno"]}'

        #
        # format entry
        #

        if self.entry:
            string += f'\ne: '
            for key, value in self.entry.items():
                string += f'{key}={value}\t'

        #
        # format exception
        #

        if self.exc:
            string += f'\nexc: {self.exc["class"]}: {self.exc["msg"]}\ntraceback:\n'
            tb = self.exc['traceback'][3:-3].split('\\n')
            tb[0] = tb[0].strip()
            for line in tb:
                string += '\t' + line.replace("', '  ", '') + '\n'

        #
        # format global
        #

        if self.global_:
            string += f'\ng: '
            if self.global_ != {}:
                for key, value in self.global_.items():
                    string += f'{key}={value}\t'

        return colored(string + '\n', get_level_color(level))

    #
    # misc
    #

    @staticmethod
    def string_trunc(string):
        length = 50
        if len(string) > length:
            return string[0:15] + ' ... ' + string[-35:]
        else:
            return string

    @property
    def level(self):
        return level_value(self.source['level'])

    @property
    def level_name(self):
        return self.source['level']
