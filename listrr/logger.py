import logging
from pathlib import Path

class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, logrecord):
        return logrecord.levelno == self.level

def log_uncaught_exceptions(ex_cls, ex, tb):
    import traceback
    logging.critical('Uncaught Exception:\n' + ''.join(traceback.format_tb(tb)))
    logging.critical(
        'An uncaught exception {0} led to critical failure. Message:\n'
        '   {1}'.format(ex_cls.__name__, ex)
    )


def setup_logger(out_dir):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    #log formatter
    formatter = logging.Formatter(
        '{threadName:10}'
        ' {asctime}'
        ' {levelname:8}'
        ' {filename}'
        ' ---  {message}'
        ,
    style='{')

    #add stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    #file handlers
    logfile = Path(out_dir) / 'log.txt'
    logfile_handler = logging.FileHandler(str(logfile))
    logfile_handler.setFormatter(formatter)
    log.addHandler(logfile_handler)

    #excepthook
    import sys
    sys.excepthook = log_uncaught_exceptions
