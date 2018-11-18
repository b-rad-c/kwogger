import logging


class KwogFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(KwogFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(KwogFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


class KwoggerAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['connid'], msg), kwargs
    
    def debug(self, *args, **kwargs):
        super().debug(*args, **kwargs)
    
    def debug_exc(self, *args, **kwargs):
        super().debug(*args, exc_info=True, **kwargs)
    
    def info(self, *args, **kwargs):
        super().info(*args, **kwargs)
    
    def info_exc(self, *args, **kwargs):
        super().info(*args, exc_info=True, **kwargs)
    
    def warning(self, *args, **kwargs):
        super().warning(*args, **kwargs)
    
    def warning_exc(self, *args, **kwargs):
        super().warning(*args, exc_info=True, **kwargs)
    
    def error(self, *args, **kwargs):
        super().error(*args, **kwargs)
    
    def error_exc(self, *args, **kwargs):
        super().error(*args, exc_info=True, **kwargs)

    def exception(self, *args, **kwargs):
        super().error(*args, exc_info=True, **kwargs)


def configure(log_file='logs/example.log'):
    fh = logging.FileHandler(log_file, 'w')
    f = KwogFormatter('%(asctime)s | %(levelname)s | %(message)s | ', '%d/%m/%Y %H:%M:%S')
    fh.setFormatter(f)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(fh)
