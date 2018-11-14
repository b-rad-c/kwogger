import os
import Kwogger
from cmd import Cmd
from termcolor import colored
import itertools


class KeyExists:
    pass


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


class KwogFileIO:

    def __init__(self, path):
        self.path = path
        self._file = open(path, 'r')

    #
    # file handler
    #

    def tell(self):
        return self._file.tell()

    def seek_head(self):
        self._file.seek(0)

    def seek_tail(self):
        self._file.seek(0, os.SEEK_END)

    def seek_line(self, lineno):
        print(f'Seek function not created: {lineno}')

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
                    yield KwogEntry.parse(line)

        except KeyboardInterrupt:
            pass

    def parse_line(self):
        """parse the next line,
        formatter: method as formatter to use a specific formatter w/o changing self._format
        :returns: str, or None if we are at EOF"""
        line = self._file.readline()
        if line:
            return KwogEntry.parse(line)

    def parse_prev(self):
        """parse the previous line
        formatter: method as formatter to use a specific formatter w/o changing self._format
        :returns str, or None if we are beginning of file"""
        pos = self.tell()
        _buffer = ''
        number_lines = 0
        # print(f'init tell: {pos}')

        while True:
            if pos == 0:
                # print(' :: return None')
                return None

            char = self._file.read(1)
            if char == '\n':
                number_lines += 1
                # print(f'pos: {pos} number lines: {number_lines}')
                if number_lines > 1:
                    # print(colored(_buffer, 'magenta'))
                    # print('')
                    # print(colored(_buffer[:0:-1]))
                    return KwogEntry.parse(_buffer[:0:-1])

            else:
                pos -= 1
                if number_lines > 0:
                    _buffer += char
                # print(f'pos: {pos} char: {char}')
                self._file.seek(pos)

    def search(self, term, direction, case_sensitive):

        parser = self.parse_prev if direction == 'up' else self.parse_line

        for n in itertools.count():
            entry = parser()
            if not entry:
                # int to signal caller that we are at EOF & the number of lines searched
                yield n
                break

            if entry.match_full_text(term, case_sensitive):
                yield entry

    def search_obj(self, query_string):
        try:
            entry = KwogEntry.parse(query_string)
            print(entry.format('data'))
            print('-----')
            print(entry.format('basic'))
        except ParseError as p:
            print(f'Parser error: {p}')


class KwogEntry:

    def __init__(self, _global=None, source=None, entry=None, exc=None, raw=None):
        self._global, self.source, self.entry, self.exc, self.raw,  = _global, source, entry, exc, raw

    def __str__(self):
        """line break between namespaces
        items = ' '.join(list(self.format_namespace('s', self.source))) + '\n'
        items += ' '.join(list(self.format_namespace('e', self.entry))) + '\n'
        if self.exc:
            items += ' '.join(list(self.format_namespace('exc', self.exc))) + '\n'
        items += ' '.join(list(self.format_namespace('g', self._global))) + '\n'
        return items"""

        items = list(self.format_namespace('s', self.source))
        items.extend(list(self.format_namespace('e', self.entry)))
        if self.exc:
            items.extend(list(self.format_namespace('exc', self.exc)))

        items.extend(list(self.format_namespace('g', self._global)))
        return ' '.join(items)

    def __iter__(self):
        for name, group in [('global', self._global), ('source', self.source), ('entry', self.entry), ('exc', self.exc)]:
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

    def format_value(self, value):
        if value is None:
            return 'None'

        if isinstance(value, (bool, float, int)):
            return str(value)

        return '"' + self.escape_value(str(value)) + '"'

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
    # match methods
    #

    def match_full_text(self, term, case_sensitive=False):
        if case_sensitive:
            return term in self.raw

        return term.lower() in self.raw.lower()

    def match_entry_object(self, match_object, case_sensitive=False):

        #
        # loop through items in match object (query params)
        #

        for name, params in dict(match_object).items():
            data = getattr(self, name)

            # if key exists continue
            if params is KeyExists:
                if data is None:
                    return False

            # match on provided dictionary params
            elif isinstance(params, dict):
                for key, value in params.items():
                    try:
                        # key exists, continue
                        if value is KeyExists and key in data:
                            continue

                        # match case insensitive strings
                        elif isinstance(value, str) and not case_sensitive:
                            if data[key].lower != value.lower():
                                return False

                        # match all other values
                        else:
                            if data[key] != value:
                                return False

                    # key not matched, return false
                    except KeyError:
                        return False

            else:
                raise ValueError('Value must be dict or KeyExists')

        # passed all filters, return true
        return True

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
        if self._global != {}:
            string += f'global: {self._global}\n'

        return string

    def _formatter_default(self):
        level = self.source["level"]

        #
        # format source line
        #

        string = f's: {self.source["time"]} {level}'
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
            string += f'\nexc: {self.exc["class"]} {self.exc["msg"]}\n\tstack: {self.exc["msg"]}'

        #
        # format global
        #

        if self._global:
            string += f'\ng: '
            if self._global != {}:
                for key, value in self.entry.items():
                    string += f'{key}={value}'

        return colored(string + '\n', Kwogger.get_level_color(level))

    #
    # misc
    #

    @staticmethod
    def string_trunc(string):
        length = 50
        if len(string) > length:
            return string[0:15] + '...' + string[-35:]
        else:
            return string


class Menu(Cmd):

    DEFAULT_FORMAT = 'default'

    def __init__(self, path, initial_cmd=None):
        self.path, self.size, self.exists = path, None, None
        self.io = KwogFileIO(self.path)
        self.format = self.DEFAULT_FORMAT
        self.initial_cmd = initial_cmd
        super().__init__()

    def preloop(self):
        self.do_status('')
        print(self.initial_cmd)
        if self.initial_cmd is not None:
            getattr(self, f'do_{self.initial_cmd}')('')

    def do_status(self, arg):
        """display info about supplied path"""
        self.size = os.path.getsize(self.path)
        self.exists = os.path.exists(self.path)

        print(f'path:      {self.path}')
        print(f'exists:    {self.exists}')
        print(f'size:      {self.size}')
        print(f'pointer:   {self.io.tell()}')

    def do_format(self, arg):
        """set formatter of Tail object, ('raw', 'data', 'basic', 'default'), supply no argument for default"""
        if arg:
            self.format = arg
        else:
            self.format(self.DEFAULT_FORMAT)

        print(f'formatter changed to: {self.format}')

    do_fmt = do_format

    def do_next(self, arg):
        """get next line or, if at EOF then run follow command"""

        # get entry
        try:
            entry = self.io.parse_line()

        except ParseError as p:
            p.parser.display_log()
            raise

        if entry is None:
            self.do_follow('')

        else:
            print(entry.format(self.format))

    do_n = do_next

    def do_prev(self, arg):
        try:
            entry = self.io.parse_prev()
        except ParseError as p:
            p.parser.display_log()
            raise

        if entry is None:
            print(colored('\n    BEGINNING OF FILE\n', 'green'))
        else:
            print(entry.format(self.format))

    do_p = do_prev

    def do_jump(self, arg):
        try:
            count = int(arg)
        except ValueError:
            count = 5

        _method = self.do_next if count > 0 else self.do_prev

        for n in range(abs(count)):
            _method('')

    do_j = do_jump

    def do_follow(self, arg):
        """seek to tail then follow supplied file, supply formatter as raw, basic (default formatter: basic)"""
        print(colored('... following ...', 'green'))

        try:
            for entry in self.io.follow():
                print(entry.format(self.format))
        except ParseError as p:
            p.parser.display_log()
            raise

    do_f = do_follow

    def do_head(self, arg):
        """seek to head of file"""
        print(f'Pointer reset to 0')
        self.io.seek_head()

    do_h = do_head

    def do_tail(self, arg):
        """seek to tail of file"""
        self.io.seek_tail()
        print(f'Pointer at tail of file: {self.io.tell()}')

    do_t = do_tail

    def do_search(self, arg):
        self.run_search(arg, 'down', False)

    do_s = do_search

    def do_search_object(self, arg):
        print('input: """{}"""\n\n'.format(arg))
        self.io.search_obj(arg)

    do_so = do_search_object

    def do_search_sensitive(self, arg):
        """search with case sensitivity"""
        self.run_search(arg, 'down', True)

    do_ss = do_search_sensitive

    def do_search_up(self, arg):
        self.run_search(arg, 'up', False)

    do_su = do_search_up

    def do_search_head(self, arg):
        self.do_head('')
        self.run_search(arg, 'down', False)

    do_sh = do_search_head

    def run_search(self, term, direction, case_sensitive):
        name = 'BOF' if direction == 'up' else 'EOF'

        if term:
            # get entry
            try:
                for n, entry in enumerate(self.io.search(term, direction, case_sensitive)):
                    if isinstance(entry, int):
                        print(colored(
                            f'\n\t{name} | tell: {self.io.tell()} | lines searched: {entry} | lines matched: {n}\n', 'white'))
                        break
                    print(entry.format(self.format))

            except ParseError as p:
                p.parser.display_log()
                raise

        else:
            print('*** No search term provided')

    def do_tell(self, arg):
        """return the pointer of the file handle"""
        print(f'Pointer at {self.io.tell()}')

    def do_q(self, arg):
        """Quits the program."""
        print('Goodbye.')
        return True
