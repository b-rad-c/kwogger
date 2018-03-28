import os
import Kwogger
from Kwogger import KwogEntry
from cmd import Cmd
from termcolor import colored


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
            return value.replace('""', '"')

        self.append_log('  > value: default')
        return str(value)

    def entry(self):
        return KwogEntry(self.data.get('g', {}), self.data.get('s', {}), self.data.get('e', {}), self.data.get('exc', {}))


class Tail:

    def __init__(self, path):
        self._format = None
        self.format_name = ''
        self.set_formatter('default')
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
    # line formatting
    #

    def set_formatter(self, formatter):
        try:
            self._format = getattr(self, f'_formatter_{formatter}')
            self.format_name = formatter

        except AttributeError:
            raise ValueError(f'Unknown formatter: {formatter}')

    def _formatter_raw(self, line):
        return line

    def _formatter_data(self, line):
        return str(Parser(line))

    def _formatter_object(self, line):
        return Parser(line)

    def _formatter_basic(self, line):
        entry = Parser(line).entry()
        string = f'source: {entry.source}\n'
        string += f'entry: {entry.entry}\n'
        if entry.exc != {}:
            string += f'exc: {entry.exc}\n'
        if entry._global != {}:
            string += f'global: {entry._global}\n'

        return string

    def _formatter_default(self, line):
        entry = Parser(line).entry()

        level = entry.source["level"][1:-1]

        #
        # format source line
        #

        string = f's: {entry.source["time"][1:-1]} {level}'
        string += f' {entry.source["path"][1:-1]} func: {entry.source["func"][1:-1]} line: {entry.source["lineno"]}'

        #
        # format entry
        #

        if entry.entry:
            string += f'\ne: '
            for key, value in entry.entry.items():
                string += f'{key}={value}\t'

        #
        # format exception
        #

        if entry.exc:
            string += f'\nexc: {entry.exc["class"]} {entry.exc["msg"]}\n\tstack: {entry.exc["msg"]}'

        #
        # format global
        #

        if entry._global:
            string += f'\ng: '
            if entry._global != {}:
                for key, value in entry.entry.items():
                    string += f'{key}={value}'

        return colored(string + '\n', Kwogger.get_level_color(level))

    #
    # methods for getting data
    #

    def follow(self):

        try:

            self.seek_tail()

            while True:
                line = self._file.readline()

                if line:
                    yield self._format(line)

        except KeyboardInterrupt:
            pass

    def parse_line(self, formatter=None):
        """parse the next line,
        formatter: method as formatter to use a specific formatter w/o changing self._format
        :returns: str, or None if we are at EOF"""
        line = self._file.readline()
        if line:
            if formatter:
                # use specific formatter
                return formatter(line)

            # use instance formatter
            return self._format(line)

    def parse_prev(self, formatter=None):
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
                    if formatter:
                        return formatter(_buffer[:0:-1])

                    # print(colored(_buffer, 'magenta'))
                    # print('')
                    # print(colored(_buffer[:0:-1]))
                    return self._format(_buffer[:0:-1])

            else:
                pos -= 1
                if number_lines > 0:
                    _buffer += char
                # print(f'pos: {pos} char: {char}')
                self._file.seek(pos)

    def search(self, key=None, value=None):
        pass


class Menu(Cmd):

    def __init__(self, path):
        self.path, self.size, self.exists = path, None, None
        self.tail = Tail(self.path)
        super().__init__()

    def preloop(self):
        self.do_status('')

    def do_status(self, arg):
        """display info about supplied path"""
        self.size = os.path.getsize(self.path)
        self.exists = os.path.exists(self.path)

        print(f'path:      {self.path}')
        print(f'exists:    {self.exists}')
        print(f'size:      {self.size}')
        print(f'pointer:   {self.tail.tell()}')

    def do_format(self, arg):
        """set formatter of Tail object, ('raw', 'data', 'basic', 'default'), supply no argument for default"""
        if arg:
            try:
                self.tail.set_formatter(arg)
            except ValueError:
                print(f'*** Unknown formatter: "{arg}"')
        else:
            self.tail.set_formatter('default')

        print(f'formatter changed to: {self.tail.format_name}')

    do_fmt = do_format

    def do_next(self, arg):
        """get next line or, if at EOF then run follow command"""

        # get entry
        try:
            entry = self.tail.parse_line()

        except ParseError as p:
            p.parser.display_log()
            raise

        if entry is None:
            print(colored('... following ...', 'green'))
            self.do_follow('')

        else:
            print(entry)

    do_n = do_next

    def do_prev(self, arg):
        try:
            entry = self.tail.parse_prev()
        except ParseError as p:
            p.parser.display_log()
            raise

        if entry is None:
            print(colored('\n    BEGINNING OF FILE\n', 'green'))
        else:
            print(entry)

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
        try:
            for entry in self.tail.follow():
                print(entry)
        except ParseError as p:
            p.parser.display_log()
            raise

    do_f = do_follow

    def do_head(self, arg):
        """seek to head of file"""
        print(f'Pointer reset to 0')
        self.tail.seek_head()

    do_h = do_head

    def do_tail(self, arg):
        """seek to tail of file"""
        self.tail.seek_tail()
        print(f'Pointer at tail of file: {self.tail.tell()}')

    do_t = do_tail

    def do_tell(self, arg):
        """return the pointer of the file handle"""
        print(f'Pointer at {self.tail.tell()}')

    def do_q(self, arg):
        """Quits the program."""
        print('Goodbye.')
        return True
