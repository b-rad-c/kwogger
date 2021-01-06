# Kwogger
[K] e y [W] o r d L [o g g e r]

By Brad Corlett

A python _LoggerAdapter_ that writes key value data to a log file while and associated classes to read and parse data 
from files while preserving type so log entries can be further processed.


Context data can be supplied at the creation of the logger to add correlating data to each log entry over the lifetime
of the logger. The first string argument to each log call is stored as key 'msg' and then every other kwarg passed to
the logging call is also added, in addition to data about the log call (file, line num, level, etc) and exception
data if relevant. Logging methods ending with _exc will automatically log exception information to save adding _exc_info_ kwarg.


    log = kwogger.rotate_by_size('log_name', 'example.log', user_id='123')
    
    x, y = 1, '1'
    
    log.info('MESSAGE', x=x, y=y)    

    try:
        x + y
    except:
        log.error_exc('should have seen this coming')
        
  ##### Convenience function for generating unique ids

    logger.generate_id(field='request_id')
    
    # each call to this logger will have a unique id added to it as field 'request_id'
    # for example to to correlate all log entries or a specific web request
    # (be sure to not share sensitive data across requests)
       
##### Longer example


    # basic
    logger.info('Sample message')
    
    # key values
    logger.info('Sample message', key1='hello', key2='world')
    
    # various data types in key values
    logger.info('Sample message', a=None, b=True, c=1, d=1.1, e='string', f=open)
    
    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        logger.error_exc('Problem dividing', x=x, y=y)

##### output to log file

    s.time="2019-02-28 23:02:15.561370" s.log="basic" s.level="INFO" s.path="examples/basic.py" s.func="<module>" s.lineno=7 e.msg="Sample message"
    s.time="2019-02-28 23:02:15.561586" s.log="basic" s.level="INFO" s.path="examples/basic.py" s.func="<module>" s.lineno=10 e.msg="Sample message" e.key1="hello" e.key2="world"
    s.time="2019-02-28 23:02:15.561749" s.log="basic" s.level="INFO" s.path="examples/basic.py" s.func="<module>" s.lineno=13 e.msg="Sample message" e.a=None e.b=True e.c=1 e.d=1.1 e.e="string" e.f="<built-in function open>"
    s.time="2019-02-28 23:11:52.021554" s.log="basic" s.level="ERROR" s.path="examples/basic.py" s.func="<module>" s.lineno=19 e.msg="Problem dividing" e.x=1 e.y=0 exc.class="ZeroDivisionError" exc.msg="division by zero" exc.traceback="""['  File """"examples/basic.py"""", line 17, in <module>\n    z = x / y\n']"""

This custom serialization format retains data type for None, bool, int, float, and str, any other value is converted to and serialized as a string. A built-in parser can deserialize read from a log file the data and retain type for post processing. 

### structure of log entries

**entry** - this is data passed to a logging method like `.info()` or `.error_exc()` The first argument to a logging call is stored added to the kwarg dictionary as key 'msg' and they are then logged together

    e.msg="Sample message" e.key1="hello" e.key2="world"

**context** - context data previously set on logger and passed to every log entry from a method like `.info()` or `.error_exc()`

    c.user_id="123"

**source** - This namespace contains information about the file and logging call such as line number and time data. 

    s.time="2019-02-28 23:02:15.561370" s.log="basic" s.level="INFO" s.path="examples/basic.py" s.func="<module>" s.lineno=7
   
**exception** - this exists when handling an exception it's data is stored in this namespace
exc._attribute_

    exc.class="ZeroDivisionError" exc.msg="division by zero" exc.traceback="""['  File """"examples/basic.py"""", line 17, in <module>\n    z = x / y\n']"""


### Parsing log files
    
    need_sample_here


    
### Built in timer
Helpful for timing long running processes to find bottle necks.

**source**

    logger.timer_start('hello', value=1)

    time.sleep(1.5)

    logger.timer_checkpoint('hello', processing=True)

    time.sleep(1.5)

    logger.timer_stop('hello', complete=True)
    
**log**
    
    s: 2019-02-28 23:33:05.161032 INFO timer1 examples/timer1.py func: main line: 20
    e: msg=TIMER_STARTED	value=1	timer_name=hello	start_time=1551425585.1610172	elapsed_time=4.76837158203125e-06
    
    s: 2019-02-28 23:33:06.662534 INFO timer1 examples/timer1.py func: main line: 24
    e: msg=TIMER_CHECKPOINT	processing=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=1.501476764678955
    
    s: 2019-02-28 23:33:08.167841 INFO timer1 examples/timer1.py func: main line: 28
    e: msg=TIMER_STOPPED	complete=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=3.006769895553589	end_time=1551425588.167787
    

### Tail utility
The built in CLI utility tails and parses the above entries and makes them more readable.

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
            
The CLI utility uses the 'termcolor' library to vary the color of each entry based on the log level.

    DEBUG=white
    INFO=green
    WARNING=yellow
    ERROR=red
    
The tail utility also has searching capabilities
    + simple search function equivalent to 'grep'ing each log entry as a line 
    + advanced search by matching key/value pair data.

Tail utility can be used by calling the module directly.
    
    python3 -m kwogger example.log
    
The utility is based on the built-in cmd module and help can be found by pressing ctrl+c while tailing and then entering '?' at the prompt.

### API Reference