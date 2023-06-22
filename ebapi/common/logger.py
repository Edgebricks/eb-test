#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


from colorlog import ColoredFormatter
import logging


def customLogger():
    """
    ebtest library for custom logger with following log levels::

        * elog.logging.tpass    - [PASS]
        * elog.logging.debug    - [DEBUG]
        * elog.logging.info     - [INFO]
        * elog.logging.warning  - [WARNING]
        * elog.logging.error    - [ERROR]
        * elog.logging.tfail    - [FAIL]

    """
    PASS      = 5
    COMMAND   = 15
    EXIT_CODE = 25
    OUTPUT    = 35
    FAIL      = 45

    lnewlevel = [(PASS, 'PASS'),
                 (COMMAND, 'COMMAND'),
                 (EXIT_CODE, 'EXIT_CODE'),
                 (OUTPUT, 'OUTPUT'),
                 (FAIL, 'FAIL')]
    for newlevel in lnewlevel:
        value, name = newlevel
        logging.addLevelName(value, name)
        setattr(logging, name, value)

    def tpass(self, *args, **kwargs):
        self.log(PASS, *args, **kwargs)
    logging.Logger.tpass = tpass

    def command(self, *args, **kwargs):
        self.log(COMMAND, *args, **kwargs)
    logging.Logger.command = command

    def texitcode(self, *args, **kwargs):
        self.log(EXIT_CODE, *args, **kwargs)
    logging.Logger.texitcode = texitcode

    def output(self, *args, **kwargs):
        self.log(OUTPUT, *args, **kwargs)
    logging.Logger.output = output

    def tfail(self, *args, **kwargs):
        self.log(FAIL, *args, **kwargs)
    logging.Logger.tfail = tfail

    logger = logging.getLogger('console')
    # create console handler
    ch = logging.StreamHandler()
    # create formatter
    fmt = '[%(asctime)s - %(log_color)s%(levelname)s%(reset)s] %(message)s\n'
    formatter = ColoredFormatter(
        fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'PASS'     : 'green',
            'DEBUG'    : 'purple',
            'COMMAND'  : 'purple',
            'INFO'     : 'blue',
            'EXIT_CODE': 'cyan',
            'OUTPUT'   : 'blue',
            'WARNING'  : 'yellow',
            'ERROR'    : 'red',
            'FAIL'     : 'red'
        }
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger and set level to DEBUG
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    return logger

elog = customLogger()
