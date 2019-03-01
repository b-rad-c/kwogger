# Kwogger
##### Requires Python 3.6+
What can I say? I love f-strings.
#### Structured logging in python
_key word logger (kw-ogger)_

An easy to use adapter for the built-in python logging library to log key value paired data that easily parseable for data analytics and monitoring with tools like splunk, ELK stack and more.

### Examples
The first argument to the log call will be stored on the entry as key 'msg'


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

This custom serialization format retains data type for None, bool, int, float, and str, any other value is converted to and serialized as a string. A built-in parser will deserialize the data and retain type for further processing. You can see that the first argument 'Sample message' is stored as key 'e.msg', e is the entry namespace, this is where user data goes. The source or 's' namespace contains information about the file, line number and time data. 
### built-in tail utility
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
    
The tail utility also has searching capabilities, both as simple 'grep'ing a string and by matching key/value pair data.

Tail utility can be used by calling the module directly.
    
    python3 -m kwogger example.log
    
The utility is based on the built-in cmd module and help can be found by pressing ctrl+c while tailing and then entering '?' at the prompt.

### Global logging variables
This library uses a logger adapter from the built in logging library which provides contextual values to the logger that the vanilla python logger does not have.

We can provide global data when initializing the logger and that data will be printed on each call to that logger over its lifetime.

    logger = kwogger.log(__name__, guid=123)
    logger.info('test')
    
When analyzing logs later all entries for this execution can be found by filtering for 'guid=123'

Convenience function for generating unique ids

    # each call to this logger will have a unique id added to it as field 'req_id'
    logger.generate_id(field='req_id')
    
### Built in timer
Helpful for timing long running processes to find bottle necks.

**source**

    logger.timer_start('hello', value=1)

    time.sleep(1.5)

    logger.timer_checkpoint('hello', processing=True
                            )
    time.sleep(1.5)

    logger.timer_stop('hello', complete=True)
    
**log**
    
    s: 2019-02-28 23:33:05.161032 INFO timer1 examples/timer1.py func: main line: 20
    e: msg=TIMER_STARTED	value=1	timer_name=hello	start_time=1551425585.1610172	elapsed_time=4.76837158203125e-06
    
    s: 2019-02-28 23:33:06.662534 INFO timer1 examples/timer1.py func: main line: 24
    e: msg=TIMER_CHECKPOINT	processing=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=1.501476764678955
    
    s: 2019-02-28 23:33:08.167841 INFO timer1 examples/timer1.py func: main line: 28
    e: msg=TIMER_STOPPED	complete=True	timer_name=hello	start_time=1551425585.1610172	elapsed_time=3.006769895553589	end_time=1551425588.167787
    
### Sensitive data
It is important to note that global data is available on this object over its life time, meaning it **should not** be re-used between requests if in a web server environment. It must be instansiated for each request to prevent data leaking to log entries spanning multiple requests.