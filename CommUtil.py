import logging
import logging.handlers

class CommUtil:
    @staticmethod
    def set_loggger(name):
        logging.basicConfig(level=logging.DEBUG)
        logger=logging.getLogger(__name__)

        LOG_FILENAME='{0}.log'.format(name)

        handler=logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=30000000,backupCount=25)

        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        handler.setLevel(logging.DEBUG)
        logger.debug('Logger set')

        return logger