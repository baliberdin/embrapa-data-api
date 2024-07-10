import os
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


def get_logger(logger_name):
    return logging.getLogger(logger_name)


# create logger
#logger = logging.getLogger(os.path.basename(__file__))

# 'application' code
#logger.debug('debug message')
#logger.info('info message')
#logger.warning('warn message')
#logger.error('error message')
#logger.critical('critical message')
