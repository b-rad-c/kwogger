# Kwogger
[K] e y [W] o r d L [o g g e r]

By Brad Corlett

#### Installation

    pip install Kwogger


#### Documentation

* sample code and log files are in ./examples
* see ./API.txt for API reference


## Description and Tutorial

A python `LoggerAdapter` that writes key value data to a log file while and associated classes to read and parse data 
from files while preserving type so log entries can be further processed.


Context data can be supplied at the creation of the logger to add correlating data to each log entry over the lifetime
of the logger. The first string argument to each log call is stored as key `msg` and then every other kwarg passed to
the logging call is also added, in addition to data about the log call (file, line num, level, etc) and exception
data if relevant. Logging methods ending with `_exc` will automatically log exception information to save adding `exc_info` kwarg. 
The order of key words as passed to the log method is preserved when written to a log for consistent readability


    log = kwogger.rotate_by_size('simple', 'simple.log', hello='world', global_context_data=True)

    # this and subsequent calls will also log kwargs from instantiation (hello='world', global_context_data=True)
    log.info('Sample message')

    log.info('Sample message', key1='hello', key2='world')

    log.info('Sample data types', a=None, b=True, c=1, d=1.1, e='string')

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        log.error_exc('Problem dividing', x=x, y=y)

**Output to log file**

    s.time="2021-01-06 21:44:19.773767" s.log="simple" s.level="INFO" s.path="./simple.py" s.func="main" s.lineno=10 e.msg="Sample message" c.hello="world" c.global_context_data=True
    s.time="2021-01-06 21:44:19.774036" s.log="simple" s.level="INFO" s.path="./simple.py" s.func="main" s.lineno=13 e.msg="Sample message" e.key1="hello" e.key2="world" c.hello="world" c.global_context_data=True
    s.time="2021-01-06 21:44:19.774152" s.log="simple" s.level="INFO" s.path="./simple.py" s.func="main" s.lineno=16 e.msg="Sample message" e.a=None e.b=True e.c=1 e.d=1.1 e.e="string" c.hello="world" c.global_context_data=True
    s.time="2021-01-06 21:44:19.774305" s.log="simple" s.level="ERROR" s.path="./simple.py" s.func="main" s.lineno=23 e.msg="Problem dividing" e.x=1 e.y=0 exc.class="ZeroDivisionError" exc.msg="division by zero" exc.traceback="""['  File """"./simple.py"""", line 20, in main\n    z = x / y\n']""" c.hello="world" c.global_context_data=True


This custom serialization format is easy to read as a log file but retains data type for `None`, `bool`, `int`, `float`, and `str`, any other value is converted to and serialized as a string. A built-in parser can deserialize read from a log file the data and retain type for post processing. 


### Initializing loggers
The `rotate_by_size` and `rotate_by_time` are convenience functions for creating a log handle, file path, level and rotation settings. It also returns and instance of `KwogAdapter` and adds kwargs to its context.

The `new` function creates a new instance of `KwogAdapter` with the specified logger. It is also able to generate a unique id and inherent context kwargs from an existing logger.
This function is useful for creating a new context for every request in a web server, by using `new` to overwrite an existing logger you can be sure data is not shared between requests.

example:

    main_log = kwogger.rotate_by_size('multi', 'multi.log', main_context=True)
    main_log.info('MESSAGE_1')

    log = kwogger.new('multi', 'request_id', main_log, first_request=True)
    log.info('MESSAGE_2')

    log = kwogger.new('multi', 'request_id', main_log, second_request=True)
    log.info('MESSAGE_3')
    
output:
    
    s.time="2021-01-24 14:17:18.624784" s.log="multiple" s.level="INFO" s.path="./multiple.py" s.func="main" s.lineno=7 c.main_context=True e.msg="MESSAGE_1"
    s.time="2021-01-24 14:17:18.628171" s.log="multiple" s.level="INFO" s.path="./multiple.py" s.func="main" s.lineno=10 c.main_context=True c.first_request=True c.request_id="c3e2588e-47f7-36a0-bbed-fe1b15ff0184" e.msg="MESSAGE_2"
    s.time="2021-01-24 14:17:18.628364" s.log="multiple" s.level="INFO" s.path="./multiple.py" s.func="main" s.lineno=13 c.main_context=True c.second_request=True c.request_id="bc0840e4-aacd-341a-aebb-6690015f2a07" e.msg="MESSAGE_3"



### Structure of log entries
Each log entry consists of four different key value dictionaries, each is explained below.

**entry**

This is data passed to a logging method like `.info()` or `.error_exc()` The first argument to a logging call is stored added to the kwarg dictionary as key `msg` and they are then logged together

    e.msg="Sample message" e.key1="hello" e.key2="world"

**context**

Context data previously set on logger and automatically passed to every log entry from a method like `.info()` or `.error_exc()`

    c.user_id="123"

**source**

This namespace contains information about the file and logging call such as line number and time data. 

    s.time="2019-02-28 23:02:15.561370" s.log="basic" s.level="INFO" s.path="examples/basic.py" s.func="<module>" s.lineno=7
   
**exception**

This exists when handling an exception, it stores the exception's `class`, `msg`, and `traceback`

    exc.class="ZeroDivisionError" exc.msg="division by zero" exc.traceback="""['  File """"examples/basic.py"""", line 17, in <module>\n    z = x / y\n']"""


### Parsing log files
The `KwogFile` class can parse log files line by line and follow a file similar to unix command `tail -f`
    
    with kwogger.KwogFile(LOG_FILE) as log:
        for entry in log:
            print(repr(entry))
            print('\tsource   ', entry.source)
            print('\tentry    ', entry.entry)
            print('\tcontext  ', entry.context)
            print('\texception', entry.exc, '\n')

Example output

    <KwogEntry | ERROR | exception=True>
	source    {'time': '2021-01-09 11:57:47.860915', 'log': 'parser', 'level': 'ERROR', 'path': './parser.py', 'func': 'write_log', 'lineno': 22}
	entry     {'msg': 'Problem dividing', 'x': 1, 'y': 0}
	context   {'pid': 40656}
	exception {'class': 'ZeroDivisionError', 'msg': 'division by zero', 'traceback': '"[\'  File ""./parser.py"", line 20, in write_log\\n    z = x / y\\n\']"'}


### CLI tail utility
The built in CLI utility uses the `KwogFile` class to follow and parse log entries entries to makes them more readable.

    s: 2019-02-28 23:02:15.561370 INFO basic examples/basic.py func: <module> line: 7
    e: msg=Sample message
    
    s: 2019-02-28 23:02:15.561586 INFO basic examples/basic.py func: <module> line: 10
    e: msg=Sample message	key1=hello	key2=world
    
    s: 2019-02-28 23:02:15.561749 INFO basic examples/basic.py func: <module> line: 13
    e: msg=Sample message	a=None	b=True	c=1	d=1.1	e=string	f=<built-in function open>
    
    s: 2019-02-28 23:11:52.021554 ERROR basic examples/basic.py func: <module> line: 19
    e: msg=Problem dividing	x=1	y=0
    exc: ZeroDivisionError: division by zero
    traceback:
        File ""examples/basic.py"", line 17, in <module>
            z = x / y
            
The CLI utility uses the `termcolor` library to vary the color of each entry based on the log level.

    DEBUG:   white
    INFO:    green
    WARNING: yellow
    ERROR:   red

Tail utility can be used by calling the module directly and providing a path
    
    python3 -m kwogger example.log
    
    # see help menu for more options
    python3 -m kwogger -h


### Convenience function for generating unique ids

    logger.generate_id(field='request_id')
    
    # each call to this logger will have a unique id added to it's context dict as key 'request_id'
    # for example to to correlate all log entries for a specific web request (make sure each request starts
    # with a new instance to prevent sharing data across multiple requests
    

### Built in timer
Helpful for timing long running processes to find bottle necks.

**source**

    log = kwogger.rotate_by_size('timer', 'timer.log')

    log.timer_start('hello', details='we are starting a timer named hello')

    time.sleep(1.5)

    log.timer_checkpoint('hello', details='we are logging a checkpoint for timer hello')
    
    time.sleep(1.5)

    log.timer_stop('hello', details='we are stopping the timer and logging the elapsed time')
    
**log**
    
    s: 2019-02-28 23:33:05.161032 INFO timer1 examples/timer1.py func: main line: 20
    e: msg=TIMER_STARTED	value=1	timer_name=hello	start_time=1551425585.1610172	elapsed_time=4.76837158203125e-06
    
    s: 2019-02-28 23:33:06.662534 INFO timer1 examples/timer1.py func: main line: 24
    e: msg=TIMER_CHECKPOINT	processing=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=1.501476764678955
    
    s: 2019-02-28 23:33:08.167841 INFO timer1 examples/timer1.py func: main line: 28
    e: msg=TIMER_STOPPED	complete=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=3.006769895553589	end_time=1551425588.167787
