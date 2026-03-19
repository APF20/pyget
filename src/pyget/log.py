import logging as Logging
from logging.handlers import RotatingFileHandler

class Logger:

    def __init__(self):
        self.loggers = {}

    def setup_custom_logger(self, name, streamLevel=Logging.WARNING, fileLevel=Logging.INFO,
                            fileName='pyget.log', maxBytes=100000000, backupCount=5):
        """
        Custom logger singleton. Defines named handlers, writes logging events to
        streaming/console/screen handler and also to file, with independant logging
        levels. Rotates log files when maxBytes reached, up to max of 5 log files.

        :param name: Required parameter. The name of the logger handler, e.g. 'root'
        :type name: str

        :param streamLevel: Streaming/console handler logging level. Default log level to
            display on screen. Options are CRITICAL (50), ERROR (40), WARNING (30),
            INFO (20), DEBUG (10), or NOTSET (0).
        :type streamLevel: Union[int, logging.level]

        :param fileLevel: File handler logging level. Log level to write to file.
        :type fileLevel: Union[int, logging.level]

        :param fileName: Absolute or relative path and filename to logfile, e.g.
            'logs/BTCUSDT.log'
        :type fileName: str

        :param maxBytes: Maximum bytes to write to a log file before rotation.
        :type fileName: int

        :param backupCount: Maximum rotated log file backups to maintain.
        :type fileName: int

        """

        if self.loggers.get(name):
            logger = self.loggers[name]

            # remove previous handlers
            for h in logger.handlers.copy():
                if isinstance(h, (RotatingFileHandler, Logging.StreamHandler)):
                    logger.removeHandler(h)

        else:
            # define handle
            if name == 'root':
                # initialise root logger with no arg/None
                logger = Logging.getLogger()
            else:
                logger = Logging.getLogger(name)

            # first filter, must be more verbose than file/stream filters
            # default is set to ERROR
            logger.setLevel('DEBUG')

            # assign new logger obj to loggers
            self.loggers[name] = logger

        # create rotating file handler
        fh = RotatingFileHandler(fileName, 'a', maxBytes=maxBytes, backupCount=backupCount)
        fh.setLevel(fileLevel)

        # create streaming/console handler
        ch = Logging.StreamHandler()
        ch.setLevel(streamLevel)

        # create formatter and add to handlers
        formatter = Logging.Formatter(fmt='%(asctime)s - %(levelname)s:%(name)s - %(module)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger
